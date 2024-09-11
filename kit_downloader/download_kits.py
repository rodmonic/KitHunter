from turtle import back
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import requests
from bs4 import BeautifulSoup, Tag

# List of search terms
search_terms = ["Kit_left_arm",
"Kit_body",
"Kit_right_arm",
"Kit_shorts"]

teams_query = """
    SELECT ?teamLabel ?wikipediaLink 
    WHERE {
        ?team wdt:P118 wd:Q9448;
            wdt:P31 wd:Q476028.
        # Retrieve the English Wikipedia link
        OPTIONAL {
        ?wikipediaLink schema:about ?team;
        schema:isPartOf <https://en.wikipedia.org/>.
        }
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    ORDER BY ?teamLabel
    """


def get_teams() -> list[tuple[str, str]]:
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

    # From https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Cats
    sparql.setQuery(teams_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    team_labels = [team['teamLabel']['value'].replace(" ", "_") for team in results['results']['bindings']]
    team_urls = [team['wikipediaLink']['value'] for team in results['results']['bindings']]
    teams = list(zip(team_urls, team_labels))
    return teams


def get_images_by_search_terms(td: Tag, search_terms: list[str]) -> list[tuple[str, str]]:

    images = []
    # Find all <img> tags within this <td>
    img_tags = td.find_all('img')

    if not img_tags:
        return images

    for term in search_terms:
        for img in img_tags:
            src = img.get('src')
            if src:
                # Check if the image filename matches any of the search terms
                background_color = get_background_color(img)
                if term in src.split('/')[-1]:  # Check if the filename contains the search term
                    full_img_url = 'https:' + src
                    images.append((full_img_url, background_color))
                    break

    return images

def get_background_color(img):
    background_color = None
    div_above = img.find_parent('div').find_previous('div')
    # Get the background-color if it exists in the inline style attribute
    if div_above and 'style' in div_above.attrs:
        styles = div_above['style']
        styles = styles.replace(" ","")
        # Look for background-color in the style attribute
        style_dict = dict(item.split(":") for item in styles.split(";") if item)

        background_color = style_dict.get('background-color', None)

    return background_color
        
    

def get_grouped_images_by_td_and_terms(url, search_terms):
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <td> tags that do not contain other <td> tags
    td_tags = [td for td in soup.find_all('td') if not td.find('td')]

    grouped_images = []

    # Loop through each <td> and find images within it by search terms
    for td in td_tags:
        images= get_images_by_search_terms(td, search_terms)
        
        # Only add this group if we found any images for any search term
        if images:
            grouped_images.append(images)

    return grouped_images

def download_images(grouped_images, team_name, year):
    # Create the team directory if it doesn't exist
    team_dir = os.path.join('downloads', team_name, str(year))
    os.makedirs(team_dir, exist_ok=True)

    # Loop through the image groups (by <td>)
    for i, group in enumerate(grouped_images, start=1):
        group_dir = os.path.join(team_dir, f'Group_{i}')
        os.makedirs(group_dir, exist_ok=True)
        
        # Loop through each search term's images in the group
        for term, images in group.items():

            # Download each image
            img_response = requests.get(images[0][0])
            if img_response.status_code == 200:
                # Save the image in the corresponding term folder
                img_filename = os.path.join(group_dir, f'{term}-{images[0][1]}.{images[0][0].split(".")[-1]}')
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_response.content)
                print(f"Downloaded {img_filename}")
            else:
                print(f"Failed to download image {images[0]}")


def download_kits(teams):

    # Loop through the list of Wikipedia URLs, get the images grouped by <td> and search terms, and download them
    for team in teams:

        for year in range(2025, 2020, -1):

            url_template = f"https://en.wikipedia.org/wiki/{year-1}–{abs(year) % 100}_{team[1]}_season"

            grouped_images = get_grouped_images_by_td_and_terms(url_template, search_terms)
            if grouped_images:
                print(f"Downloading images for team {team}...")
                download_images(grouped_images, team[1], year)
            else:
                print(f"No images matching search terms found for team {team[1]}.")


if __name__ == "__main__":
    teams = get_teams()
    download_kits(teams)