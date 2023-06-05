from django.contrib import admin
from .models import Carrusel, Slide, InternalLink, Parallax, PortadaVideo, VideosPortada
from django.contrib.admin.widgets import FilteredSelectMultiple
from .forms import CarruselForm
from django.core.exceptions import ValidationError



class InternalLinkInline(admin.StackedInline):
    model = InternalLink
    extra = 1

class SlideAdmin(admin.ModelAdmin):
    inlines = [InternalLinkInline]

class CarruselAdmin(admin.ModelAdmin):
    form = CarruselForm


class VideosPortadainLine(admin.StackedInline):
    model = VideosPortada

class PortadaVideoAdmin(admin.ModelAdmin):
    inlines = [VideosPortadainLine]



admin.site.register(Carrusel, CarruselAdmin)
admin.site.register(Slide,SlideAdmin)
admin.site.register(Parallax)
admin.site.register(PortadaVideo, PortadaVideoAdmin)