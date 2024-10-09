from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import League, Team, Kit, KitColor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'hashed_password']  # List of fields to include in the serializer
        extra_kwargs = {'hashed_password': {'write_only': True}}  # Don't return the hashed password in responses


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class KitColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitColor
        fields = ['id', 'part', 'red', 'green', 'blue', 'kit']


class KitSerializer(serializers.ModelSerializer):
    kitcolors = KitColorSerializer(many=True, read_only=True)  # Nested serializer for kit colors

    class Meta:
        model = Kit
        fields = ['id', 'kit_type', 'season', 'sponsor', 'team', 'slug', 'kitcolors']


class TeamSerializer(serializers.ModelSerializer):
    kits = KitSerializer(many=True, read_only=True)  # Nested serializer for kits

    class Meta:
        model = Team
        fields = ['id', 'name', 'league', 'wiki_link', 'country', 'kits']
        depth = 1  # This will include related league details


class LeagueSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)  # Nested serializer for related teams

    class Meta:
        model = League
        fields = ['id', 'league_name', 'level', 'teams']  # Include related teams


class KitColorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitColor
        fields = ['id', 'part', 'red', 'green', 'blue', 'kit']  # Serializer for creating KitColor instances


class KitWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = ['id', 'kit_type', 'season', 'sponsor', 'team', 'slug']  # Serializer for creating Kit instances


class TeamWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'league', 'wiki_link', 'country']  # Serializer for creating Team instances


class LeagueWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'league_name', 'level']  # Serializer for creating League instances
