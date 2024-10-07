from django.db import models


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=255)  # CharField used for ID
    email = models.EmailField(unique=True, db_index=True)  # EmailField with unique and index
    hashed_password = models.CharField(max_length=255)  # CharField for hashed passwords


class League(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing integer ID
    league_name = models.CharField(max_length=255)  # CharField for the league name
    level = models.CharField(max_length=255)  # CharField for league level

    def __str__(self):
        return self.league_name


class Team(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing integer ID
    name = models.CharField(max_length=255)  # CharField for the team name
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")  # ForeignKey to League
    wiki_link = models.URLField(max_length=255, blank=True, null=True)  # URLField for wiki link
    country = models.CharField(max_length=255)  # CharField for country

    def __str__(self):
        return self.name


class Kit(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing integer ID
    kit_type = models.CharField(max_length=255)  # CharField for kit type (e.g., "Home", "Away")
    season = models.IntegerField()  # IntegerField for season
    sponsor = models.CharField(max_length=255, blank=True, null=True)  # CharField for sponsor
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="kits")  # ForeignKey to Team
    slug = models.SlugField(max_length=255)  # SlugField for slug


class KitColor(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing integer ID
    part = models.CharField(max_length=255)  # CharField for the part of the kit (e.g., shirt, shorts)
    red = models.IntegerField()  # IntegerField for red value in RGB
    green = models.IntegerField()  # IntegerField for green value in RGB
    blue = models.IntegerField()  # IntegerField for blue value in RGB
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="kitcolors")  # ForeignKey to Kit
