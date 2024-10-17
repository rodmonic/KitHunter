from data_gathering import slugify, run_query
from image_funcs import convert_svg_to_png  # fill_in_background_color
from time import strftime
import logging
from data_gathering import get_leagues_from_query, get_teams_from_query, kit_exists

import os
import sys

import requests
from bs4 import BeautifulSoup

import mwclient
import urllib

import django

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kit_hunter.settings')
django.setup()


from app.models import Team, League, Kit, KitPart, KitPartColor  # noqa: E402


user_agent = 'KitHunter/0.1 (dominic.mccaskill@gmail.com)'
site = mwclient.Site('commons.wikimedia.org', clients_useragent=user_agent)
image_dir = "./frontend/public/images/"

# List of search terms
kit_parts = [
    "Kit_left_arm",
    "Kit_body",
    "Kit_right_arm"
]

image_map = {
    '31px-Kit_left_arm.svg.png': "Kit_left_arm.svg",
    '31px-Kit_right_arm.svg.png': "Kit_right_arm.svg",
    '38px-Kit_body.svg.png': "Kit_body.svg"
}


def get_images_by_kit_part(soup, kit_parts: list[str]) -> list[tuple[str, str]]:

    images = {}
    # Find all <img> tags within this <td>
    img_tags = soup.find_all('img')

    if not img_tags:
        return images

    for kit_part in kit_parts:
        kit_part_images = soup.find_all('img', src=lambda src: src and kit_part in src)

        for img in kit_part_images:
            src = img.get('src')
            if src:
                if kit_part in src.split('/')[-1]:  # Check if the filename contains the search term
                    # Check if the image filename matches any of the search terms
                    div_above = img.find_parent('div').find_previous('div')
                    background_color = get_background_color(div_above)
                    if not background_color:
                        div_above = img.find_parent('div')
                        background_color = get_background_color(div_above)

                    kit_type = get_kit_type(img)
                    if kit_type:
                        full_img_url = 'https:' + src
                        if kit_type in images:
                            images[kit_type].append((kit_part, full_img_url, background_color))
                        else:
                            images[kit_type] = [(kit_part, full_img_url, background_color)]

    # Delete multiple entries for the same kit type

    return images


def get_kit_type(img):

    try:
        kit_type_div = img.find_parent('div').find_parent('div').find_next_sibling('div').find_all('a')[0]
        kit_type = kit_type_div.text
    except (IndexError):
        kit_type_div = img.find_parent('div').find_parent('div').find_next_sibling('div').find_all('b')[0]
        kit_type = kit_type_div.text
    except (AttributeError):
        kit_type = ""

    return slugify(kit_type)


def get_background_color(div):
    background_color = None
    # Get the background-color if it exists in the inline style attribute

    if div and 'style' in div.attrs:
        styles = div['style'].replace(" ", "")
        # Look for background-color in the style attribute
        style_dict = dict(item.split(":") for item in styles.split(";") if item)
        background_color = None
        if 'background-color' in styles:
            background_color = style_dict.get('background-color', None)

    return background_color


def get_kit_type_images(url, kit_parts):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    kit_types = {}

    # Loop through each <td> and find images within it by search terms

    images = get_images_by_kit_part(soup, kit_parts)

    # Only add this group if we found any images for any search term
    if images:
        kit_types.update(images)

    return kit_types


def create_kits(season, kit_type_images, team_id):

    for kit_type, images in kit_type_images.items():

        new_kit = Kit(
            kit_type=kit_type,
            season=season,
            sponsor=None,
            team_id=team_id
        )

        new_kit.save()

        # Loop through each search term's images in the group
        for kit_part, image_name, background_color in images:

            image_name = image_name.split("/")[-1]
            image_name = urllib.parse.unquote(image_name)
            image_name = image_map.get(image_name, image_name)
            image = site.images[image_name]
            image_path = os.path.join(image_dir, image_name)

            if not image.exists:
                print(f"Image {image_name} does not exist on Wikimedia Commons.")
                continue

            # if not in cache then download it
            if not os.path.isfile(image_path):
                try:
                    with open(image_path, 'wb') as img_file:
                        image.download(img_file)
                except Exception as e:
                    raise e

            # if the file is svg then convert to png as save
            image_path = convert_svg_to_png(image_path, image_dir)

            if KitPart.objects.all().filter(kit_part__exact=kit_part).filter(kit=new_kit).exists():
                continue

            new_kit_part = KitPart(
                kit_part=kit_part,
                image_name=image_name,
                background_color=background_color,
                kit=new_kit
            )

            new_kit_part.save() 


def download_club_kits(teams, start_year):

    logging.debug("DOWLOAD KITS|GET IMAGES")

    # Loop through the list of Wikipedia URLs, get the images grouped by <td> and search terms, and download them
    for team in teams:
        team_id = team['teamID']['value']
        try:
            teamLabel = team['wikipediaLink']['value'].split('/')[-1]
        except KeyError:
            continue

        logging.debug(f"DOWLOAD KITS|GET IMAGES|{teamLabel}")

        for year in range(2025, start_year - 1, -1):

            season = f'{year}-{str(year-1)[2:4]}'
            logging.debug(f"DOWLOAD KITS|GET IMAGES|{teamLabel}|{year}")

            if not kit_exists(season, team_id):

                # First try the current season
                url_template = f"https://en.wikipedia.org/wiki/{year-1}–{abs(year) % 100}_{teamLabel}_season"
                kit_images = get_kit_type_images(url_template, kit_parts)

                # if that doesn't exist and we're in the first year then try
                if not kit_images and year == 2025:
                    url_template = f"https://en.wikipedia.org/wiki/{teamLabel}"
                    kit_images = get_kit_type_images(url_template, kit_parts)

                if kit_images:

                    print(f"Downloading images for team {team['teamLabel']['value']} - {season}...")
                    create_kits(
                        season,
                        kit_images,
                        team_id
                    )

                else:
                    logging.debug(f"DOWLOAD KITS|GET IMAGES|{teamLabel}|{year}|No images matching search terms found for team {teamLabel} and {year}.")


logging.basicConfig(
    filename=f'./kit_scraper/logging/{strftime("%Y%m%d-%H%M%S")}.log',
    encoding='utf-8',
    level=logging.DEBUG
)


if __name__ == "__main__":
    logging.debug("START")
    logging.debug("RUN QUERY")

    if True:
        # process leagues
        logging.debug("Get Leagues")
        leagues = run_query('./kit_scraper/queries/all_leagues.sparql')
        get_leagues_from_query(leagues)

    if True:
        # process teams
        logging.debug("Get Teams")
        teams = run_query('./kit_scraper/queries/all_teams.sparql')
        get_teams_from_query(teams)

    # process kits
    logging.debug("DOWNLOAD KITS")

    # Start the download process

    if True:
        download_club_kits(teams, 2020)
        logging.debug("PREPARE DATA")

    if True:
        pass
        # get kit colours
