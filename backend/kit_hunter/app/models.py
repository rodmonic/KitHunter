# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class League(models.Model):
    id = models.CharField(primary_key=True, max_length=300)
    league_name = models.CharField(max_length=100)
    level = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'league'

    def __str__(self):
        return self.league_name


class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=300)
    name = models.CharField(max_length=30)
    league = models.ForeignKey(League, models.CASCADE)
    wiki_link = models.CharField(blank=True, null=True, max_length=100)
    country = models.CharField(blank=True, null=True, max_length=100)

    class Meta:
        db_table = 'team'

    def __str__(self):
        return self.name


class Kit(models.Model):
    kit_type = models.CharField(max_length=10)
    season = models.IntegerField(blank=True, null=True)
    sponsor = models.CharField(blank=True, null=True, max_length=50)
    team = models.ForeignKey(Team, models.CASCADE)
    slug = models.CharField(max_length=500)

    class Meta:
        db_table = 'kit'

    def __str__(self):
        return self.slug


class KitColor(models.Model):
    part = models.CharField(max_length=15)
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()
    kit = models.ForeignKey(Kit, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'kitcolor'
