from django.contrib import admin
from .models import League, Team, Kit, KitColor

# Register models with customizations
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Kit)
admin.site.register(KitColor)