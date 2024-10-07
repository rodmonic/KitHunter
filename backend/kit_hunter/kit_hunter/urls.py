from rest_framework.routers import DefaultRouter
from django.urls import path, include
from app.views import UserViewSet, LeagueViewSet, TeamViewSet, KitViewSet, KitColorViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'kits', KitViewSet)
router.register(r'kitcolors', KitColorViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include all the routes from the router
]
