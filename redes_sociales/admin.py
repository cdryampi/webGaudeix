from django.contrib import admin
from .models import RedSocial

class RedSocialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'link', 'fondo')

admin.site.register(RedSocial, RedSocialAdmin)