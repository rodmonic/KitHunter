from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import Group, User
from .models import League, Team, Kit, KitColor
from .serializers import (
    LeagueSerializer, LeagueWriteSerializer,
    TeamSerializer, TeamWriteSerializer, KitSerializer,
    KitWriteSerializer, KitColorSerializer, KitColorWriteSerializer,
    GroupSerializer, UserSerializer
)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class DistinctCountriesView(APIView):
    def get(self, request):
        # Get distinct countries from the database
        countries = Team.objects.values_list('country', flat=True).distinct()
        return Response(list(countries))  # Return as a list


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LeagueWriteSerializer
        return LeagueSerializer  # Read operations use the read serializer

    def get_queryset(self):
        queryset = super().get_queryset()  # Call the base implementation first
        country = self.request.query_params.get('country', None)  # Get the 'country' query parameter

        if country:
            queryset = queryset.filter(country__iexact=country)  # Adjust as per your field names

        return queryset


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TeamWriteSerializer
        return TeamSerializer

    def get_queryset(self):
        queryset = super().get_queryset()  # Call the base implementation first
        league_id = self.request.query_params.get('league_id', None)  # Get the 'country' query parameter

        if league_id:
            queryset = queryset.filter(league_id__exact=league_id)  # Adjust as per your field names

        return queryset


class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KitWriteSerializer
        return KitSerializer

    def get_queryset(self):
        queryset = super().get_queryset()  # Call the base implementation first
        team_id = self.request.query_params.get('team_id', None)  # Get the 'country' query parameter

        if team_id:
            queryset = queryset.filter(team_id__exact=team_id)  # Adjust as per your field names

        return queryset


class KitColorViewSet(viewsets.ModelViewSet):
    queryset = KitColor.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KitColorWriteSerializer
        return KitColorSerializer
