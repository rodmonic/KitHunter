from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from app.views import LeagueViewSet, TeamViewSet, KitViewSet, KitColorViewSet, DistinctCountriesView, CustomAuthToken
from app.views import UserViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'kits', KitViewSet)
router.register(r'kitcolors', KitColorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),  # Include all the routes from the router
    path('accounts/', include("django.contrib.auth.urls")),
    path('api/auth/token/', CustomAuthToken.as_view(), name='api_auth_token'),
    path('api/v1/countries/', DistinctCountriesView.as_view(), name='distinct-countries'),
]
