from .models import League, Team, Kit, KitColor
from .serializers import (
    LeagueSerializer, LeagueWriteSerializer,
    TeamSerializer, TeamWriteSerializer, KitSerializer,
    KitWriteSerializer, KitColorSerializer, KitColorWriteSerializer,
    GroupSerializer, UserSerializer
)

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


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
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LeagueWriteSerializer
        return LeagueSerializer  # Read operations use the read serializer

    def get_queryset(self):
        queryset = super().get_queryset()  # Call the base implementation first
        country = self.request.query_params.get('country', None)  # Get the 'country' query parameter

        if country:
            queryset = queryset.filter(country__iexact=country).order_by('level')  # Adjust as per your field names

        return queryset

    @action(detail=False, methods=['get'], url_path=r'countries')
    def unique_countries(self, request, team_id=None):
        """
        Custom action to get custom countries
        """
        # Get distinct countries from the database
        countries = League.objects.exclude(country__isnull=True).values_list('country', flat=True).distinct().order_by('country')
        return Response(list(countries))  # Return as a list


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TeamWriteSerializer
        return TeamSerializer

    def get_queryset(self):
        queryset = super().get_queryset()  # Call the base implementation first
        league_id = self.request.query_params.get('league_id', None)  # Get the 'country' query parameter

        if league_id:
            queryset = queryset.filter(league_id__exact=league_id).order_by('name')  # Adjust as per your field names

        return queryset


class KitViewSet(viewsets.ModelViewSet):
    queryset = Kit.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KitWriteSerializer
        return KitSerializer

    def list(self, request, *args, **kwargs):
        """
        Overrides the default list method to support filtering by team_id and season.
        """
        queryset = self.queryset
        team_id = kwargs.get('team_id', None)
        season = kwargs.get('season', None)

        if team_id:
            queryset = queryset.filter(team_id__exact=team_id)

        if season:
            queryset = queryset.filter(season=season)

        # Serialize the filtered queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'(?P<team_id>[^/.]+)')
    def list_by_team(self, request, team_id=None):
        """
        Custom action to list kits filtered by team_id.
        """
        queryset = self.queryset.filter(team_id=team_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'(?P<team_id>[^/.]+)/(?P<season>\d+)')
    def list_by_team_and_season(self, request, team_id=None, season=None):
        """
        Custom action to list kits filtered by team_id and season.
        """
        queryset = self.queryset.filter(team_id=team_id, season=season)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='seasons')
    def get_seasons(self, request):
        """
        Custom action to get distinct seasons for a given team.
        """
        team_id = self.request.query_params.get('team_id', None)

        if not team_id:
            return Response({"detail": "Team parameter is required."}, status=400)

        queryset = self.queryset.filter(team_id__exact=team_id)
        seasons = queryset.values_list('season', flat=True).distinct().order_by('-season')

        return Response(list(seasons))


class KitColorViewSet(viewsets.ModelViewSet):
    queryset = KitColor.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KitColorWriteSerializer
        return KitColorSerializer
