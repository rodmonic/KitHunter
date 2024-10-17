from django.contrib import admin
from .models import League, Team, Kit, KitPart, KitPartColor

# Register models with customizations
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Kit)
admin.site.register(KitPart)
admin.site.register(KitPartColor)
