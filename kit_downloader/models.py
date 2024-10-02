from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class League(SQLModel, table=True):

    id: str = Field(default=None, primary_key=True)  # Primary key
    league_name: str
    level: Optional[int] = None

    # Relationships
    teams: list["Team"] = Relationship(back_populates="league")


class Team(SQLModel, table=True):

    id: str = Field(default=None, primary_key=True)  # Primary key
    name: str
    league_id: Optional[str] = Field(default=None, foreign_key="league.id")  # Foreign key
    wiki_link: Optional[str]
    country: Optional[str]

    # Relationships
    league: League | None = Relationship(back_populates="teams")


class Kit(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key
    kit_type: str  # e.g., "Home", "Away", "Third"
    season: Optional[str] = None
    sponsor: Optional[str] = None
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")  # Foreign key
    slug: str


class KitColor(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key
    part: str
    red: int
    green: int
    blue: int
    kit_id: Optional[int] = Field(default=None, foreign_key="kit.id")  # Foreign key
