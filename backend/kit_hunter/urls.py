from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from knox import views as knox_views
from app.views import LeagueViewSet, TeamViewSet, KitViewSet, KitPartViewSet, KitPartColorViewSet
from app.views import UserViewSet, GroupViewSet, LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'kits', KitViewSet)
router.register(r'kit_parts', KitPartViewSet)
router.register(r'kit_part_colors', KitPartColorViewSet)


urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),  # Include all the routes from the router
    path('accounts/', include("django.contrib.auth.urls")),
    path('kits/', KitViewSet.as_view({'get': 'list'}), name='kit-list'),
]
