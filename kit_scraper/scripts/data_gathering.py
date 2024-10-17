from image_funcs import detect_dominant_colors

import unicodedata
import re
import os
import sys
from typing import Any, Dict, List, Optional
import json


from SPARQLWrapper import SPARQLWrapper, JSON

import django


sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kit_hunter.settings')
django.setup()


from app.models import Team, League, Kit, KitPart, KitPartColor  # noqa: E402


def safe_get(d: Dict[str, Any], keys: List[str]) -> Optional[Any]:
    for key in keys:
        d = d.get(key)
        if d is None:
            return None
    return d


def run_query(file_path: str) -> list[tuple[str, str]]:

    cache_file = file_path.replace(".sparql", ".json")

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    with open(file_path, 'r') as file:
        query = file.read()  # Read the entire content of the file

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Save to cache file
    with open(cache_file, 'w') as f:
        json.dump(results['results']['bindings'], f)

    return results['results']['bindings']


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


# process leagues
def get_leagues_from_query(leagues):

    for league in leagues:
        if not league_exists(league['league']['value']):
            new_league = League(
                id=league['league']['value'],
                league_name=league['leagueLabel']['value'],
                level=safe_get(
                    league, ['level', 'value']
                ),
            )
            new_league.save()


def get_teams_from_query(teams):

    for team in teams:
        if not team_exists(team['teamID']['value']):
            new_team = Team(
                id=team['teamID']['value'],
                name=team['teamLabel']['value'],
                wiki_link=safe_get(
                    team, ['wikipediaLink', 'value']
                ),
                country=safe_get(
                    team, ['countryLabel', 'value']
                ),
                league_id=team['leagueID']['value']
            )
            new_team.save()


# def get_colors_from_kits():

#     kits = Kit.objects.all()
#     for kit in tqdm(kits):

#         for file in os.listdir(kit.slug):

#             split_file = file.split(".")

#             file_mask = f'./masks/{split_file[0]}_mask.{split_file[1]}'
#             try:
#                 dominant_colors = detect_dominant_colors(os.path.join(kit.slug, file), file_mask, 3)
#             except Exception as e:
#                 if e:
#                     dominant_colors = []

#             for color in dominant_colors:
#                 new_kit_colour = KitColor(
#                     part=split_file[0].replace(" ", "_"),
#                     kit_id=kit.id,
#                     red=color[0],
#                     green=color[1],
#                     blue=color[2]
#                 )
#                 new_kit_colour.save()


def league_exists(id: str) -> bool:
    return League.objects.all().filter(id=id).exists()


def team_exists(id: str) -> bool:
    return Team.objects.all().filter(id=id).exists()


def kit_exists(season: int, team_id: str) -> bool:
    return Kit.objects.all().filter(team_id=team_id).filter(season=season).exists()
