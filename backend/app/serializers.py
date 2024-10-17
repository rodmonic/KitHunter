from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import League, Team, Kit, KitPart, KitPartColor


# Users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'hashed_password']  # List of fields to include in the serializer
        extra_kwargs = {'hashed_password': {'write_only': True}}  # Don't return the hashed password in responses


# Groups
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


# read serialisers
class KitPartColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitPartColor
        fields = ['id', 'color']


class KitPartSerializer(serializers.ModelSerializer):
    colors = KitPartColorSerializer(many=True, read_only=True, source='kitpartcolor_set')

    class Meta:
        model = KitPart
        fields = ['id', 'kit_part', 'image_name', 'background_color', 'kit', 'colors']


class KitSerializer(serializers.ModelSerializer):
    parts = KitPartSerializer(many=True, read_only=True, source='kitpart_set')

    class Meta:
        model = Kit
        fields = ['id', 'kit_type', 'season', 'sponsor', 'team', 'parts']


class TeamSerializer(serializers.ModelSerializer):
    kits = KitSerializer(many=True, read_only=True, source='kit_set')

    class Meta:
        model = Team
        fields = ['id', 'name', 'league', 'wiki_link', 'country', 'kits']


class LeagueSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True, source='team_set')

    class Meta:
        model = League
        fields = ['id', 'league_name', 'level', 'country', 'teams']


# Write Serialisers
class LeagueWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'league_name', 'level', 'country']


class TeamWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'league', 'wiki_link', 'country']


class KitWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = ['kit_type', 'season', 'sponsor', 'team']


class KitPartWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitPart
        fields = ['kit_part', 'image', 'background_color', 'kit']


class KitPartColorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitPartColor
        fields = ['color', 'kit']
