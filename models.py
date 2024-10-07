from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, Index=True)
    hashed_password = Column(String)


class League(Base):
    __tablename__ = "league"

    id = Column(Integer, primary_key=True)  # Primary key
    league_name = Column(String)
    level = Column(String)

    # Relationships
    teams = relationship("Team", back_populates="league")


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True)  # Primary key
    name = Column(String)
    league_id = Column(String, foreign_key="league.id")  # Foreign key
    wiki_link = Column(String)
    country = Column(String)

    # Relationships
    league = relationship("League", back_populates="teams")
    kits = relationship("Kit", back_populates="team")


class Kit(Base):
    __tablename__ = "kit"

    id = Column(Integer, primary_key=True)  # Primary key
    kit_type = Column(String)  # e.g., "Home", "Away", "Third"
    season = Column(Integer)
    sponsor = Column(String)
    team_id = Column(String, foreign_key="teams.id")  # Foreign key
    slug = Column(String)

    # Relationships
    team = relationship("Team", back_populates="kits")
    kitcolors = relationship("KitColor", back_populates="kit")


class KitColor(Base):
    __tablename__ = "kitcolor"

    id = Column(Integer, primary_key=True)  # Primary key
    part = Column(String)
    red = Column(Integer)
    green = Column(Integer)
    blue = Column(Integer)
    kit_id = Column(Integer, foreign_key="kit.id")  # Foreign key

    # Relationships
    kit = relationship("Kits", back_populates="kitcolours")

