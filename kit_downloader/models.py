from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Team(SQLModel, table=True):
    
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key
    wd_id: str
    name: str
    country: Optional[str]
    league_id: Optional[int] = Field(default=None, foreign_key="league.id")  # Foreign key
    wiki_link: str

    # Relationships
    # kits: List["Kit"] = Relationship(back_populates="team")

class KitColor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key
    color_name: str  # e.g., "Red", "Blue", "#FFFFFF"
    hex_code: str
    kit_id: Optional[int] = Field(default=None, foreign_key="kit.id")  # Foreign key

class Kit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key
    kit_type: str  # e.g., "Home", "Away", "Third"
    season: Optional[str] = None
    sponsor: Optional[str] = None
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")  # Foreign key

    # Relationship to Team
    # team: Optional[Team] = Relationship(back_populates="kits")

    # # Relationship to KitColor
    # left_arm_colors: List[KitColor] = Relationship(back_populates="kits_left_arm")
    # right_arm_colors: List[KitColor] = Relationship(back_populates="kits_right_arm")
    # body_colors: List[KitColor] = Relationship(back_populates="kits_body")

class League(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key
    wd_id: str
    league_name: str
    level: Optional[int] = None
    country: Optional[str] = None
