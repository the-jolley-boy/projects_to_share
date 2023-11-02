from django.contrib import admin
from discordlogin.models import DiscordUser

# Register your models here.
class DiscordUserAdmin(admin.ModelAdmin):
    list_display = ["id", "discord_tag", "last_login"]
    pass

admin.site.register(DiscordUser, DiscordUserAdmin)
