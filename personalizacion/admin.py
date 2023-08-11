from django.contrib import admin
from .models import Carrusel, Slide, InternalLink, Parallax, VideosEmbed
from django.contrib.admin.widgets import FilteredSelectMultiple
from .forms import CarruselForm
from django.core.exceptions import ValidationError
from multimedia_manager.models import Video


class InternalLinkInline(admin.StackedInline):
    model = InternalLink
    extra = 1



class SlideAdmin(admin.ModelAdmin):
    inlines = [InternalLinkInline]

class CarruselAdmin(admin.ModelAdmin):
    form = CarruselForm





admin.site.register(Carrusel, CarruselAdmin)
admin.site.register(Slide,SlideAdmin)
admin.site.register(Parallax)
admin.site.register(VideosEmbed)
