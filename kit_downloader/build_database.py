from sqlmodel import create_engine, SQLModel, Session
from models import Team, KitColor, Kit, League
import os


def create_db_and_tables(engine):

    SQLModel.metadata.create_all(engine)


def add_team_with_kit_and_colors(engine):
    """
    Adds a Team, assigns it a Kit, and adds multiple KitColors to the Kit.
    """
    with Session(engine) as session:
        # Create a Team instance
        team = Team(
            name="Dream FC",
            country="Fictionland",
            founded_year=2020,
            stadium="Dream Stadium"
        )
        session.add(team)
        session.commit()
        session.refresh(team)  # Refresh to get the generated ID
        print(f"Added Team: {team.name} with ID: {team.id}")

        # Create a Kit instance and assign it to the Team via relationship
        kit = Kit(
            kit_type="Home",
            sponsor="DreamCorp"
        )
        team.kits.append(kit)  # Automatically sets kit.team_id to team.id

        # Create KitColor instances and assign them to the Kit via relationship
        color1 = KitColor(color_name="White")
        color2 = KitColor(color_name="Blue")
        kit.colors.extend([color1, color2])  # Automatically sets color.kit_id to kit.id

        # Add the Kit and KitColors to the session
        session.add(team)  # Team and related Kits and KitColors are added due to relationships
        session.commit()
        session.refresh(kit)
        print(f"Added Kit: {kit.kit_type} Kit with Sponsor: {kit.sponsor} and ID: {kit.id}")
        print(f"Added KitColors: {[color.color_name for color in kit.colors]} to Kit ID: {kit.id}")


def main():
    """
    Main function to orchestrate database creation, data insertion, and querying.
    """
    # Define the database file path
    db_file = "football_team.db"
    db_url = f"sqlite:///{db_file}"

    # Remove the existing database file if it exists for a fresh start
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing database file: {db_file}")

    # Create a SQLite engine with echo=True to display SQL statements
    engine = create_engine(db_url, echo=True)

    # Create the database and tables
    create_db_and_tables(engine)

    # Add a Team with Kit and KitColors
    add_team_with_kit_and_colors(engine)


if __name__ == "__main__":
    main()

