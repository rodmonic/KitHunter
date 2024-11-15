from .models import League, Team, Kit, KitPart, KitPartColor, UserKitLog
from .serializers import (
    LeagueSerializer, LeagueWriteSerializer,
    TeamSerializer, TeamWriteSerializer, KitSerializer,
    KitWriteSerializer, KitPartColorSerializer, KitPartColorWriteSerializer,
    KitPartSerializer, KitPartWriteSerializer, GroupSerializer, UserSerializer,
    UserKitLogSerializer, UserKitLogWriteSerializer
)

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from random import randint


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

    def list(self, request):
        queryset = Kit.objects.all()

        # Filter by league
        league_id = request.query_params.get('league_id', None)
        if league_id != 'null':
            queryset = queryset.filter(team__league__id=league_id)

        # Filter by team
        team_id = request.query_params.get('team_id', None)
        if team_id != 'null':
            queryset = queryset.filter(team__id=team_id)

        # Filter by country
        country = request.query_params.get('country', None)
        if country != 'null':
            queryset = queryset.filter(team__country=country)

        # Filter by season
        season = request.query_params.get('season', None)
        if season != 'null':
            queryset = queryset.filter(season=season)

        # Filter by kit type
        kit_type = request.query_params.get('kitType', None)
        if kit_type != 'null':
            queryset = queryset.filter(kit_type=kit_type)

        # get number of records to return
        number = request.query_params.get('number', None)
        if number != 'null':
            int_number = int(number)
            queryset_length = len(queryset)
            if int_number < queryset_length:
                start = randint(0, queryset_length - int_number)
                queryset = queryset[start:start + int_number]

        # Serialize the filtered queryset
        serializer = KitSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'(?P<team_id>[^/.]+)')
    def list_by_team(self, request, team_id=None):
        """
        Custom action to list kits filtered by team_id.
        """
        queryset = self.queryset.filter(team_id=team_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path=r'(?P<team_id>[^\/.]+)\/(?P<season>[^\/.]+)')
    def list_by_team_and_season(self, request, team_id=None, season=None):
        """
        Custom action to list kits filtered by team_id and season.
        """
        queryset = self.queryset.filter(team=team_id, season=season)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='kit_types')
    def get_kit_types(self, request):
        """
        Custom action to get distinct kit_types for a given team and season.
        """
        team_id = self.request.query_params.get('team_id', None)
        season = self.request.query_params.get('season', None)

        if not team_id:
            return Response({"detail": "Team parameter is required."}, status=400)

        if not season:
            return Response({"detail": "Season parameter is required."}, status=400)

        queryset = self.queryset.filter(team_id__exact=team_id).filter(season__exact=season)
        kit_types = queryset.values_list('kit_type', flat=True).distinct().order_by('-season')

        return Response(list(kit_types))

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


class KitPartViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing KitPart instances.
    """
    queryset = KitPart.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, kit_id=None):
        if kit_id is not None:
            return KitPart.objects.filter(kit_id=kit_id)
        return KitPart.objects.none()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KitPartWriteSerializer
        return KitPartSerializer

    @action(detail=False, methods=['get'], url_path=r'(?P<kit_id>[^/.]+)')
    def list_by_team(self, request, kit_id=None):
        """
        Custom action to list kit_parts filtered by Kit_id.
        """
        queryset = self.queryset.filter(kit_id=kit_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='batch')
    def batch_retrieve(self, request):
        """
        Custom action to retrieve multiple KitPart instances based on a list of kit_ids provided in the request body.
        """
        # Extract `kit_ids` from the request body
        kit_ids = request.data.get('kit_ids')

        # Check if `kit_ids` was provided and is a list
        if not kit_ids or not isinstance(kit_ids, list):
            return Response(
                {"detail": "kit_ids must be provided as a list."},
                status=400
            )

        # Filter the queryset by the provided kit_ids
        queryset = KitPart.objects.filter(kit_id__in=kit_ids)

        # Serialize and return the filtered queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class KitPartColorViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing KitPartColor instances.
    """
    queryset = KitPartColor.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # Use different serializers for reading and writing
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KitPartColorWriteSerializer
        return KitPartColorSerializer


class UserKitLogViewSet(viewsets.ModelViewSet):
    queryset = UserKitLog.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserKitLogWriteSerializer
        return UserKitLogSerializer

    def perform_create(self, serializer):
        # Assign the user from the request to the 'user' field
        serializer.save(user=self.request.user)


class UserStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        # Query and join relevant data
        user_logs = UserKitLog.objects.filter(user_id=user_id).select_related('team', 'team__league')

        # Create a list of dictionaries to hold data for DataFrame
        data = []
        for log in user_logs:
            data.append({
                'team': log.team.name,
                'league': log.team.league.league_name,
                'date_spotted': log.time,
                'country': log.team.country,
                'kit_type': log.kit_type,
                'season': log.season
                # add more fields as needed from related models
            })

        return Response(data)
