from SPARQLWrapper import SPARQLWrapper, JSON
import unicodedata
import re

from sqlmodel import SQLModel, Session, select
from typing import Any, Dict, List, Optional

from models import League, Team, Kit

def safe_get(d: Dict[str, Any], keys: List[str]) -> Optional[Any]:
    for key in keys:
        d = d.get(key)
        if d is None:
            return None
    return d

def run_query(file_path: str) -> list[tuple[str, str]]:

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    with open(file_path, 'r') as file:
        query = file.read()  # Read the entire content of the file
     
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

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
def get_leagues_from_query(leagues, engine):

    with Session(engine) as session:

        for league in leagues:
            if not league_exists(session, league['league']['value']):
                new_league = League(
                    id = league['league']['value'],
                    league_name = league['leagueLabel']['value'],
                    level = safe_get(
                        league, ['level','value']
                    ),
                )
                session.add(new_league)
        
        session.commit()


def get_teams_from_query(teams, engine):

    with Session(engine) as session:

        for team in teams:
            if not team_exists(session, team['team']['value']):
                new_team = Team(
                    id = team['team']['value'],
                    name = team['teamLabel']['value'],
                    wiki_link = safe_get(
                        team, ['wikipediaLink', 'value']
                    ),
                    country = safe_get(
                        team, ['countryLabel', 'value']
                    ),
                    league_id = team['league']['value']
                )
                session.add(new_team)
        
        session.commit()


def get_kits_from_query(kit: str, year: int, team_id: Team, slug: str, engine):

    with Session(engine) as session:

        new_kit = Kit(
        kit_type = kit,
        season = year,
        team_id = team_id,
        slug = slug + f'/{kit}/'
        )
        
        session.add(new_kit)
        session.commit()


def league_exists(session: Session, id: str) -> bool:
    statement = select(League).where(League.id == id)
    result = session.exec(statement).first()  # Use .first() to return only one record, if exists
    return result is not None


def team_exists(session: Session, id: str) -> bool:
    statement = select(Team).where(Team.id == id)
    result = session.exec(statement).first()  # Use .first() to return only one record, if exists
    return result is not None

