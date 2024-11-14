from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import League, Team, Kit, KitPart, KitPartColor, UserKitLog


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

    class Meta:
        model = KitPart
        fields = ['id', 'kit_part', 'image_name', 'background_color', 'kit']


class KitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kit
        fields = ['id', 'kit_type', 'season', 'sponsor', 'team']


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['id', 'name', 'league', 'wiki_link', 'country']


class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ['id', 'league_name', 'level', 'country']


class UserKitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKitLog
        fields = ['id', 'team', 'time', 'season', 'kit_type', 'latitude', 'longitude']


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


class UserKitLogWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKitLog
        fields = ['team', 'time', 'season', 'kit_type', 'latitude', 'longitude']
