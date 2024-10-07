from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, League, Team, Kit, KitColor
from .serializers import (
    UserSerializer, LeagueSerializer, LeagueWriteSerializer,
    TeamSerializer, TeamWriteSerializer, KitSerializer,
    KitWriteSerializer, KitColorSerializer, KitColorWriteSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LeagueWriteSerializer
        return LeagueSerializer  # Read operations use the read serializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TeamWriteSerializer
        return TeamSerializer


class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KitWriteSerializer
        return KitSerializer


class KitColorViewSet(viewsets.ModelViewSet):
    queryset = KitColor.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KitColorWriteSerializer
        return KitColorSerializer