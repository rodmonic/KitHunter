
from time import strftime
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import requests
from bs4 import BeautifulSoup
import unicodedata
import re
from PIL import Image
import mwclient
import shutil
import urllib
import logging
import cairosvg

logging.basicConfig(filename=f'./logging/{strftime("%Y%m%d-%H%M%S")}.log', encoding='utf-8', level=logging.DEBUG)

user_agent = 'KitHunter/0.1 (dominic.mccaskill@gmail.com)'
site = mwclient.Site('commons.wikimedia.org', clients_useragent=user_agent)
cache_dir = "./cache/"

# List of search terms
kit_parts = ["Kit_left_arm",
"Kit_body",
"Kit_right_arm"]

image_map={
    '31px-Kit_left_arm.svg.png' : "Kit_left_arm.svg",
    '31px-Kit_right_arm.svg.png' : "Kit_right_arm.svg",
    '38px-Kit_body.svg.png' : "Kit_body.svg"
}


with open('./queries/all_leagues.sparql', 'r') as file:
    sparql_query = file.read()  # Read the entire content of the file


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def run_query(query: str) -> list[tuple[str, str]]:
    """
    Fetches a list of sports teams from Wikidata along with their corresponding Wikipedia URLs.

    This function sends a SPARQL query to the Wikidata SPARQL endpoint to retrieve sports team information.
    It processes the results to extract team labels and their associated Wikipedia links, returning a list
    of tuples where each tuple contains:
        - A Wikipedia URL (str) for the team.
        - A formatted team label (str) with spaces replaced by underscores.

    Returns:
        list[tuple[str, str]]: A list of tuples where each tuple contains a Wikipedia URL and a team label.
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results['results']['bindings']


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
                        images[kit_type]= [(kit_part, full_img_url, background_color)]
                    break
    
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


def convert_svg_to_png(file_path, output_folder):
    # Check if the file is an SVG
    if not file_path.lower().endswith('.svg'):
        return file_path  # Return original path if not an SVG

    # Get the base name (without extension) and the full output path
    base_name = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    png_file_path = os.path.join(output_folder, f"{file_name_without_ext}.png")

    # Check if the PNG already exists
    if os.path.exists(png_file_path):
        return png_file_path  # Return PNG path if it already exists

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Convert the SVG to PNG and save it
    try:
        cairosvg.svg2png(url=file_path, write_to=png_file_path)
        print(f"Converted {file_path} to {png_file_path}")
        return png_file_path  # Return the path to the newly created PNG
    except Exception as e:
        print(f"Error converting SVG to PNG: {e}")
        return file_path  # Return the original path if an error occurs

def hex_to_rgb(hex_color: str) -> tuple:
    """
    Converts a hex color string (e.g., '#FF5733') to an RGB tuple (R, G, B).
    
    Args:
        hex_color (str): The hex color string, optionally prefixed with '#'.
        
    Returns:
        tuple: A tuple representing the RGB color.
    """
    hex_color = hex_color.lstrip('#')  # Remove the '#' if present
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    else:
        raise ValueError(f"Invalid hex color code: {hex_color}")


def fill_in_background_color(file, color):
    # Define the new background color (R, G, B)
    
    try:
        background_color = hex_to_rgb(color)  # Red background
    except ValueError:
        logging.debug(f"DOWLOAD KITS|Fill In Background Color|Error|{file}, {color}")   
        return
    
    # Open the existing image
    existing_image = Image.open(file)

    # Get the size of the existing image
    width, height = existing_image.size

    # Create a new image with the same size and the background color
    background = Image.new('RGB', (width, height), background_color)

    # Paste the existing image onto the background
    # We use the alpha channel if the existing image has transparency
    background.paste(existing_image, (0, 0), existing_image.convert('RGBA'))

    # Save the new image
    background.save(file)


def download_kits(teams):

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
            
                print(f"Downloading images for team {team['teamLabel']['value']}...")
                download_images(
                    slugify(team['countryLabel']['value']),
                    slugify(team['leagueLabel']['value']),
                    slugify(team['teamLabel']['value']), 
                    year,
                    kit_images, 
                )
            else:
                logging.debug(f"DOWLOAD KITS|GET IMAGES|{teamLabel}|{year}|No images matching search terms found for team {teamLabel} and {year}.")



if __name__ == "__main__":
    logging.debug("START")
    logging.debug("RUN QUERY")
    leagues_and_teams = run_query(sparql_query)
    logging.debug("DOWLOAD KITS")
    download_kits(leagues_and_teams)