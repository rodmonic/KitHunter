from data_gathering import slugify, run_query
from image_funcs import convert_svg_to_png, fill_in_background_color
from time import strftime
import logging
from data_gathering import get_leagues_from_query, get_teams_from_query, get_kits_from_query, get_colors_from_kits


from sqlmodel import create_engine, SQLModel, Session
import os
import requests
from bs4 import BeautifulSoup

import mwclient
import shutil
import urllib

from models import KitColor, Kit, League, Team


user_agent = 'KitHunter/0.1 (dominic.mccaskill@gmail.com)'
site = mwclient.Site('commons.wikimedia.org', clients_useragent=user_agent)
cache_dir = "./cache/"

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
                    full_img_url = 'https:' + src
                    if kit_type in images:
                        images[kit_type].append((kit_part, full_img_url, background_color))
                    else:
                        images[kit_type] = [(kit_part, full_img_url, background_color)]

    if images:
        pass

    return images


def get_kit_type(img):

    try:
        kit_type_div = img.find_parent('div').find_parent('div').find_next_sibling('div').find_all('a')[0]
        kit_type = kit_type_div.text
    except (IndexError):
        kit_type_div = img.find_parent('div').find_parent('div').find_next_sibling('div').find_all('b')[0]
        kit_type = kit_type_div.text
    except (AttributeError):
        kit_type = "error"

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


def download_images(country_label, league_label, team_name, year, kit_type_images):

    logging.debug(f"DOWLOAD KITS|GET IMAGES||{country_label}|{league_label}|{team_name}|{year}")
    # Create the team directory if it doesn't exist
    team_dir = os.path.join('downloads', country_label, league_label, team_name, str(year))
    os.makedirs(team_dir, exist_ok=True)

    # Loop through the image groups (by <td>)
    for kit_type, images in kit_type_images.items():
        group_dir = os.path.join(team_dir, kit_type)
        os.makedirs(group_dir, exist_ok=True)

        file_count = len([f for f in os.listdir(group_dir) if os.path.isfile(os.path.join(group_dir, f))])

        if file_count >= 3:
            logging.debug(f"DOWNLOAD KITS|GET IMAGES||{country_label}|{league_label}|{team_name}|{year}|Skipped")
            continue

        # Loop through each search term's images in the group
        for kit_part, image_name, background_color in images:

            image_name = image_name.split("/")[-1]
            decoded_image_name = urllib.parse.unquote(image_name)
            mapped_image_name = image_map.get(decoded_image_name, decoded_image_name)
            image = site.images[mapped_image_name]

            if not image.exists:
                logging.debug(f"DOWNLOAD KITS|GET IMAGES|{country_label}|{league_label}|{team_name}|{year}|{kit_part}|Does Not Exist on Wikipedia")
                print(f"Image {image_name} does not exist on Wikimedia Commons.")
                continue

            # first check if image exists in the cache.
            cache_path = os.path.join(cache_dir, mapped_image_name)

            # if not in cache then download it
            if not os.path.isfile(cache_path):
                try:
                    with open(cache_path, 'wb') as img_file:
                        image.download(img_file)
                        logging.debug(f"DOWNLOAD KITS|GET IMAGES|{country_label}|{league_label}|{team_name}|{year}|{kit_part}|Dowloaded from Wikipedia to Cache")
                except Exception as e:
                    raise e

            # if the file is svg then convert to png as save
            cache_path = convert_svg_to_png(cache_path, cache_dir)

            try:
                # copy the image from the cache to the corresponding team folder
                img_filename = os.path.join(group_dir, f'{kit_part}.{cache_path.split(".")[-1]}')

                # if file already downloaded then cancel out
                if os.path.isfile(img_filename):
                    continue

                shutil.copyfile(cache_path, img_filename)
                logging.debug(f"DOWLOAD KITS|GET IMAGES||{country_label}|{league_label}|{team_name}|{year}|{kit_part}|Copied from Cache")
                if background_color:
                    fill_in_background_color(img_filename, background_color)

                print(f"Downloaded {mapped_image_name} as {img_filename}")

            except Exception as e:
                logging.debug(f"DOWLOAD KITS|GET IMAGES||{country_label}|{league_label}|{team_name}|{year}|{kit_part}|Failed to get Image")
                print(f"Failed to get image for {mapped_image_name}: {e}")


def download_kits(teams, engine):

    logging.debug("DOWLOAD KITS|GET IMAGES")

    # Loop through the list of Wikipedia URLs, get the images grouped by <td> and search terms, and download them
    for team in teams:

        try:
            teamLabel = team['wikipediaLink']['value'].split('/')[-1]
        except KeyError:
            continue

        logging.debug(f"DOWLOAD KITS|GET IMAGES|{teamLabel}")

        for year in range(2025, 2024, -1):

            logging.debug(f"DOWLOAD KITS|GET IMAGES|{teamLabel}|{year}")

            # First try the current season
            url_template = f"https://en.wikipedia.org/wiki/{year-1}–{abs(year) % 100}_{teamLabel}_season"
            kit_images = get_kit_type_images(url_template, kit_parts)

            # if that doesn't exist and we're in the first year then try
            if not kit_images and year == 2025:
                url_template = f"https://en.wikipedia.org/wiki/{teamLabel}"
                kit_images = get_kit_type_images(url_template, kit_parts)

            if kit_images:
                country_slug = slugify(team['countryLabel']['value'])
                league_slug = slugify(team['leagueLabel']['value'])
                team_slug = slugify(team['teamLabel']['value'])

                print(f"Downloading images for team {team['teamLabel']['value']}...")
                download_images(
                    country_slug,
                    league_slug,
                    team_slug,
                    year,
                    kit_images,
                )

                slug = f"./downloads/{country_slug}/{league_slug}/{team_slug}"

                for kit, _ in kit_images.items():
                    get_kits_from_query(kit, year, team['team']['value'], slug, engine)

            else:
                logging.debug(f"DOWLOAD KITS|GET IMAGES|{teamLabel}|{year}|No images matching search terms found for team {teamLabel} and {year}.")


logging.basicConfig(
    filename=f'./logging/{strftime("%Y%m%d-%H%M%S")}.log',
    encoding='utf-8',
    level=logging.DEBUG
)

if __name__ == "__main__":
    logging.debug("START")
    logging.debug("RUN QUERY")

    # set up SQLModel
    engine = create_engine("sqlite:///football_team.db", echo=True)

    # delete any tables that might need readding
    SQLModel.metadata.drop_all(engine, tables=[KitColor.__table__])
    SQLModel.metadata.drop_all(engine, tables=[Kit.__table__])
    SQLModel.metadata.drop_all(engine, tables=[Team.__table__])
    SQLModel.metadata.drop_all(engine, tables=[League.__table__])

    # create table
    SQLModel.metadata.create_all(engine)

    # process leagues
    leagues = run_query('./queries/all_leagues.sparql')
    get_leagues_from_query(leagues, engine)

    # process teams
    teams = run_query('./queries/all_teams.sparql')
    get_teams_from_query(teams, engine)

    # process kits
    logging.debug("DOWNLOAD KITS")

    # Start the download process
    download_kits(teams, engine)
    logging.debug("PREPARE DATA")

    get_colors_from_kits(engine)
