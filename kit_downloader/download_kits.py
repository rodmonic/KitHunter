from SPARQLWrapper import SPARQLWrapper, JSON
import os
import requests
from bs4 import BeautifulSoup, Tag
import unicodedata
import re
from PIL import Image


# List of search terms
kit_parts = ["Kit_left_arm",
"Kit_body",
"Kit_right_arm",
"Kit_shorts"]

sparql_query = """
SELECT DISTINCT ?countryLabel ?level ?league ?leagueLabel ?team ?teamLabel
WHERE {
  {   
  ?league wdt:P31 wd:Q15991303. 
  ?league p:P361 ?statement.   
  ?statement ps:P361 ?league_system;
             pq:P3983 ?level.
  ?league_system wdt:P17 ?country.
  ?pq_qual wikibase:qualifier pq:P3983.  
    
  # Linking teams to the league
  ?team wdt:P118 ?league.  # Team plays in the league
  
  # Exclude items that have a specific property, e.g., P1234
  FILTER NOT EXISTS {
    ?league wdt:P576 ?value.  # Property P1234 should not be present
  }
     
  }
UNION
  {
  ?league wdt:P31 wd:Q15991303;   # Instance of football league
          wdt:P3983 ?level;  # Direct sports league level assignment
          wdt:P17 ?country.
  # Linking teams to the league
  ?team wdt:P118 ?league.  # Team plays in the league
    
  FILTER NOT EXISTS {
    ?league wdt:P576 ?value.  # Property P1234 should not be present
  }
    
  }
  # Filter for levels 1, 2, or 3
  FILTER(?level IN (1, 2, 3))


  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}

ORDER BY ?countryLabel ?level
    """

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

    # team_labels = [team['teamLabel']['value'].replace(" ", "_") for team in results['results']['bindings']]
    # team_urls = [team['wikipediaLink']['value'] for team in results['results']['bindings']]
    # teams = list(zip(team_urls, team_labels))
    return results['results']['bindings']


def get_images_by_kit_part(td: Tag, kit_parts: list[str]) -> list[tuple[str, str]]:

    images = {}
    # Find all <img> tags within this <td>
    img_tags = td.find_all('img')

    if not img_tags:
        return images

    for kit_part in kit_parts:
        for img in img_tags:
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

    return images

def get_kit_type(img):

    try:
        kit_type_div = img.find_parent('div').find_parent('div').find_next_sibling('div').find_all('a')[0]
        kit_type = kit_type_div.text
    except IndexError:
        kit_type_div = img.find_parent('div').find_parent('div').find_next_sibling('div').find_all('b')[0]
        kit_type = kit_type_div.text
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
    
    # Find all <td> tags that do not contain other <td> tags
    td_tags = [td for td in soup.find_all('td') if not td.find('td')]

    kit_types = {}

    # Loop through each <td> and find images within it by search terms
    for td in td_tags:
        images = get_images_by_kit_part(td, kit_parts)

        # Only add this group if we found any images for any search term
        if images:
            kit_types.update(images)

    return kit_types

def download_images(country_label, league_label, team_name, year, kit_type_images):
    # Create the team directory if it doesn't exist
    team_dir = os.path.join('downloads', country_label, league_label, team_name, str(year))
    os.makedirs(team_dir, exist_ok=True)

    # Loop through the image groups (by <td>)
    for kit_type, images in kit_type_images.items():
        group_dir = os.path.join(team_dir, kit_type)
        os.makedirs(group_dir, exist_ok=True)
        
        # Loop through each search term's images in the group
        for kit_part, image_url, background_color in images:

            # Download each image
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                # Save the image in the corresponding term folder
                img_filename = os.path.join(group_dir, f'{kit_part}.{image_url.split(".")[-1]}')
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_response.content)
                if background_color:
                    fill_in_background_color(img_filename, background_color)
                print(f"Downloaded {img_filename}")
            else:
                print(f"Failed to download image {images[0]}")


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

    # Loop through the list of Wikipedia URLs, get the images grouped by <td> and search terms, and download them
    for team in teams:

        teamLabel = team['teamLabel']['value'].replace(" ", "_")

        for year in range(2025, 2024, -1):

            url_template = f"https://en.wikipedia.org/wiki/{year-1}–{abs(year) % 100}_{teamLabel}_season"
            kit_images = get_kit_type_images(url_template, kit_parts)

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
                print(f"No images matching search terms found for team {teamLabel} and {year}.")


if __name__ == "__main__":
    leagues_and_teams = run_query(sparql_query)
    download_kits(leagues_and_teams)