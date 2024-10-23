from django.db import models
from django.conf import settings


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
    season = models.CharField(max_length=7, blank=True, null=True)
    sponsor = models.CharField(blank=True, null=True, max_length=50)
    team = models.ForeignKey(Team, models.CASCADE)

    class Meta:
        db_table = 'kit'

    def __str__(self):
        return self.slug


class KitPart(models.Model):
    kit_part = models.CharField(max_length=10, null=True, blank=True)
    image_name = models.CharField(max_length=50, null=True, blank=True)
    background_color = models.CharField(max_length=7, default=None)
    kit = models.ForeignKey(Kit, models.CASCADE)

    class Meta:
        db_table = 'kit_part'


class KitPartColor(models.Model):
    color = models.CharField(max_length=7, default=None)
    kit = models.ForeignKey(KitPart, models.CASCADE)

    class Meta:
        db_table = 'kit_part_color'


class UserKitLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    team = models.ForeignKey(Team, models.CASCADE, blank=True, null=True)
    kit = models.ForeignKey(Kit, models.CASCADE, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'user_kit_log'
