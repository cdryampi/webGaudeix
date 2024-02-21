from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Q
from multimedia_manager.models import Imagen, Fichero, Audio
from .models import Agenda, VisitaGuiada, Ruta, VariationAgenda, CertificadoTurismoSostenible, Idioma, AudioRuta, PlayListRuta, Alojamiento, Restaurante
from map.models import MapPoint
from django.forms import DurationField
from blog.models import PostImagen, PostGaleriaImagen, PostFichero, Categoria, Tag
from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from blog.admin_modulos.admin_post import PostImagenInline

class RutaAudioInline(admin.TabularInline):
    model = AudioRuta
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'audio':
            playlist_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                playlist_id = request.resolver_match.kwargs['object_id']
            kwargs['queryset'] = Audio.objects.filter(
                Q(audioruta__isnull=True) | Q(audioruta__playlist=playlist_id)
            )
            kwargs['empty_label'] = 'sense àudio viculat'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PlayListRutaInline(admin.TabularInline):
    model = PlayListRuta
    extra = 1
    inlines = [RutaAudioInline]


class PostGaleriaImagenInline(admin.TabularInline):
    model = PostGaleriaImagen
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            agenda_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                agenda_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Imagen.objects.filter(
                Q(postgaleriaimagen__isnull=True) | Q(postgaleriaimagen__post__id=agenda_id),
                Q(subcategoriagaleriaimagen__isnull=True),
                Q(subcategoriabannerimagen__isnull=True),
                Q(categoriabannerimagen__isnull=True),
                Q(subblogimagen__isnull=True),
                Q(subbloggaleriaimagen__isnull=True),
                Q(categoriagaleriaimagen__isnull=True),
                Q(postimagen__isnull=True),
                Q(eventoespecialgaleriaimagen__isnull=True),
                Q(diversidadimagenbanner__isnull=True),
                Q(compradescubrepasosimagen__isnull=True),
                Q(compradescubreimagen__isnull=True),
                Q(compradescubregaleriaimagen__isnull=True),
                Q(alerta__isnull=True)
            )
            kwargs['empty_label'] = 'Sin imagen asociada'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class VariationAgendaInline(admin.TabularInline):
    model = VariationAgenda
    extra = 0

class PostFicheroImagenInline(admin.TabularInline):
    model = PostFichero
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'fichero':
            agenda_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                agenda_id = request.resolver_match.kwargs['object_id']

            kwargs['queryset'] = Fichero.objects.filter(
                Q(postfichero__isnull=True) | Q(postfichero__post__id=agenda_id),
                Q(eventofichero__isnull=True),
                Q(pdfcollectionresoluciofichero__isnull =True),
                Q(pdfcollectionjustificaciofichero__isnull=True),
                Q(pdfcollectionconvocatoriafichero__isnull=True),
                Q(pdfcollectiontotesfichero__isnull = True),
                Q(pdfdiversidadfichero__isnull=True),
                Q(compradescubrefichero__isnull=True),
                Q(alerta__isnull=True)
            )
            kwargs['empty_label'] = 'Sense fitxer associat'

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PostImagenInlineRuta(admin.TabularInline):
    model = PostImagen
    extra = 1
    readonly_fields = ['imagen_preview']

    def imagen_preview(self, instance):
        if instance.imagen:
            return instance.imagen.archivo.imagen_thumbnail()
        return '(Cap imatge associada)'

    imagen_preview.short_description = 'Imatge associada'
    # Agregar help_text al campo 'imagen'
    fieldsets = [
        (None, {
            'fields': ['imagen'],
            'description': "Seleccioneu la imatge que es farà servir com a miniatura i principal."
        }),
    ]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'imagen':
            post_id = None
            if hasattr(request, 'resolver_match') and 'object_id' in request.resolver_match.kwargs:
                post_id = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = Imagen.objects.filter(
                    Q(subcategoriagaleriaimagen__isnull=True),
                    Q(subcategoriabannerimagen__isnull=True),
                    Q(alerta__isnull=True),
                    Q(categoriabannerimagen__isnull=True),
                    Q(subblogimagen__isnull=True),
                    Q(subbloggaleriaimagen__isnull=True),
                    Q(categoriagaleriaimagen__isnull=True),
                    Q(categoriabannerimagen__isnull=True),
                    Q(postgaleriaimagen__isnull=True),
                    Q(eventoespecialgaleriaimagen__isnull=True),
                    Q(diversidadimagenbanner__isnull=True),
                    Q(compradescubrepasosimagen__isnull=True),
                    Q(compradescubreimagen__isnull=True),
                    Q(compradescubregaleriaimagen__isnull=True),
                    Q(postimagen__isnull=True) | Q(postimagen__post__id=post_id)
                )
            kwargs['empty_label'] = 'Sense imatge associada'
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PlayListAdmin(admin.ModelAdmin):
    model = PlayListRuta
    inlines = [RutaAudioInline]




class AgendaAdmin(TranslationAdmin, admin.ModelAdmin):
    inlines = [PostGaleriaImagenInline, VariationAgendaInline, PostFicheroImagenInline]
    autocomplete_fields = ['ubicacion',]
    filter_horizontal = ('tags','idiomas')
    search_fields = ['titulo']
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'metatitulo',
                'descripcion',
                'metadescripcion',
                'descripcion_corta',
                'categoria',
                'publicado',
                'ubicacion',
                'entradas',
                'idiomas',
                'tipo_evento',
                'tags'
                ],

            'description': (
                "<p><strong><em>Aquesta és l'administració d'una Agenda.</em></strong></p>"
                "<p><em>Aquí pots introduir totes les dades relacionades amb la teva agenda. "
                "Assegura't d'omplir tots els camps necessaris amb la informació correcta.</em></p>"
                "<p><em>Recorda que aquests camps estan destinats a recollir informació sobre l'agenda, "
                "com el <strong>títol</strong>, la <strong>descripció</strong>, la <strong>ubicació</strong> i altres detalls importants.</em></p>"
                "<p><em>També pots marcar l'opció <strong>entrades</strong> si hi ha entrades disponibles per a l'esdeveniment.</em> Sortirà un enllaç cap a Codetiquets.</p>"
                "<p><em>Assegura't d'afegir tags amb sentit perquè es faran servir per al <strong>SEO</strong> i per mostrar característiques del calendari en PDF que es genera.</em></p>"
                "<p><strong>Properes Activitats:</strong> A la pàgina del portal, els esdeveniments més propers seran destacats a la secció de 'Properes Activitats', oferint als usuaris una vista ràpida de les properes activitats programades.</p>"
                "<p><em>El camp <strong>tipo_evento</strong> et permet seleccionar el tipus d'esdeveniment de l'agenda, com 'Música', 'Teatre', 'Exposició', etc.</em></p>"
            ),


        }),
        # Resto de los fieldsets
    ]


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(tipo="agenda")
        return super(AgendaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'tipo_evento':
            kwargs['help_text'] = _("Selecciona el tipus d'esdeveniment")
        return super(AgendaAdmin, self).formfield_for_dbfield(db_field, request, **kwargs)





class VisitaGuidadaForm(forms.ModelForm):
    duracion_dias = forms.IntegerField(help_text="Duració en dies", required=False)
    duracion_horas = forms.IntegerField(help_text="Duració en hores", required=False)


    class Meta:
        model = VisitaGuiada
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.duracion:
            duracion = self.instance.duracion
            duracion_dias = duracion.days
            duracion_horas = duracion.seconds // 3600
            self.initial['duracion_dias'] = duracion_dias
            self.initial['duracion_horas'] = duracion_horas

    def clean(self):
        cleaned_data = super().clean()
        duracion_dias = cleaned_data.get('duracion_dias')
        duracion_horas = cleaned_data.get('duracion_horas')

        duracion = timedelta()

        if duracion_dias:
            duracion += timedelta(days=duracion_dias)

        if duracion_horas:
            duracion += timedelta(hours=duracion_horas)

        cleaned_data['duracion'] = duracion

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        duracion_dias = self.cleaned_data.get('duracion_dias')
        duracion_horas = self.cleaned_data.get('duracion_horas')

        if duracion_dias is not None and duracion_horas is not None:
            duracion = timedelta(days=duracion_dias, hours=duracion_horas)
            instance.duracion = duracion

        if commit:
            instance.save()

        return instance




class VisitaGuidadaAdmin(TranslationAdmin, admin.ModelAdmin):
    form = VisitaGuidadaForm
    inlines = [PostImagenInlineRuta, PostGaleriaImagenInline, PostFicheroImagenInline]
    filter_horizontal = ('agendas','tags','certificados')
    autocomplete_fields = ['mapa', 'categoria']
    
    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'metatitulo',
                'descripcion',
                'metadescripcion',
                'publicado',
                'categoria',
                'precio',
                'certificados',
                'fecha_inicio',
                'fecha_fin',
                'duracion_dias',
                'duracion_horas',
                'publico_recomendado',
                'mostrar_calendario',
                'mapa',
                'agendas',
                'tags'
                ],

            'description': (
                "<p><strong><em>Aquesta és l'administració d'una Visita Guiada.</em></strong></p>"
                "<p><em>Aquí pots introduir totes les dades relacionades amb la teva visita guiada. "
                "Assegura't d'omplir tots els camps necessaris amb la informació correcta.</em></p>"
                "<p><em>Recorda que aquests camps estan destinats a recollir informació sobre la visita, "
                "com el <strong>preu</strong>, la <strong>duració</strong>, les <strong>dates</strong> i altres detalls importants.</em></p>"
                "<p><em>Tingues en compte que si les dates de <strong>inici</strong> i <strong>fi</strong> estan invertides, "
                "el <strong>calendari</strong> pot no funcionar com esperat. A més, si la data passada és més gran que la de <strong>inici</strong>, "
                "pot haver-hi problemes amb les <strong>dates</strong>.</em></p>"
                "<p><em>Si l'event no té <strong>preu</strong>, pots deixar-lo a 0,00, i el sistema el detectarà com a gratuït.</em></p>"
                "<p><em>Recordeu que cal activar manualment el <strong>calendari</strong> perquè es mostri en el calendari a la web en <strong>mostrar calendari</strong>.</em></p>"
                "<p><em>Assegura't d'afegir tags amb sentit perquè es faran servir per al <strong>SEO</strong>.</em></p>"
            ),

        }),
        # Resto de los fieldsets
    ]
    
    exclude = ['duracion']  # Excluir el campo duracion en el administrador







class RutaAdmin(TranslationAdmin, admin.ModelAdmin):
    form = VisitaGuidadaForm
    inlines = [PostGaleriaImagenInline, PostFicheroImagenInline, PostImagenInlineRuta]
    exclude = ['duracion']  # Excluir el campo duracion en el administrador
    autocomplete_fields = ['categoria','punto_inicio','mapas_itinerario', 'subcategoria']
    filter_horizontal = ('tags', 'playlist')

    fieldsets = [
        (None,{
            'fields':[
                'titulo',
                'metatitulo',
                'descripcion',
                'metadescripcion',
                'publicado',
                'pendiente',
                'categoria',
                'subcategoria',
                'distancia',
                'tema',
                'actividad',
                'valoracion',
                'tipologia',
                'dificultad',
                'punto_inicio',
                'mapas_itinerario',
                'playlist',
                'enlace_natura_local',
                'tags',
            ],
            'description': (
            "<p><strong><em>Aquesta és l'administració d'una Ruta.</em></strong></p>"
            "<p><em>Aquí pots introduir totes les dades relacionades amb la teva ruta. "
            "Assegura't d'omplir tots els camps necessaris amb la informació correcta.</em></p>"
            "<p><em>Recorda que aquests camps estan destinats a recollir informació sobre la ruta, "
            "com la <strong>durada</strong>, la <strong>pendent</strong>, la <strong>distància</strong>, i altres detalls importants.</em></p>"
            "<p><em>També pots especificar la <strong>tipologia</strong> i la <strong>dificultat</strong> de la ruta per ajudar els usuaris a trobar les rutes que més els interessen.</em></p>"
            "<p><em>El punt d'inici de la ruta es pot especificar mitjançant el <strong>Punt d'inici</strong> seleccionat.</em></p>"
            "<p><em>Pots afegir mapes que formen part de l'itinerari amb els <strong>Mapes d'itinerari</strong>.</em></p>"
            "<p><em>L'enllaç a Natura Local et permet vincular a una pàgina específica de Natura Local on es poden trobar més detalls sobre la ruta.</em></p>"
            "<p><em>Assegura't d'afegir tags amb sentit perquè es faran servir per al <strong>SEO</strong>.</em></p>"
            "<p><strong>Nota important:</strong> Perquè aquesta ruta respecti tots els camps del model, és necessari que estigui associada a la categoria <strong>'Senderisme'</strong> o seleccioni <strong>'Senderisme que existeix'</strong> a la secció de 'Categoria'.</p>"
            "<p><strong>Properes Rutes:</strong> Les properes rutes seran destacades a la secció de 'Properes Rutes' al portal, oferint als usuaris una vista ràpida de les pròximes rutes programades.</p>"
        ),

        })
    ]





class CertificadoTurismoSostenibleAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,{
            'fields':[
                'nombre',
                'descripcion',
                'logo',
                'ods_relacionados',
                'enlace_externo'
            ],
            'description': (
            "<p><strong><em>Aquesta és l'administració dels certificats.</em></strong></p>"
            "<p><em>Aquí pots afegir un logo de turisme sostenible que apliquen a aquesta visita guiada.</em></p>"
            "<p><em>Recorda que aquests camps estan destinats a recollir informació sobre el certificat.</em></p>"
            "<p><em>També pots assignar un ODS que té relació amb el certificat.</p>"
            "<p><em>Pots afegir un enllaç extern cap a l'empresa certificadora.</em></p>"
        ),

        })
    ]

class IdiomaAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,{
            'fields':[
                'nombre',
                'codigo',
                'descripcion'
            ],
            'description': (
            "<p><strong><em>Aquesta és l'administració dels idiomes.</em></strong></p>"
            "<p><em>Aquí pots afegir un idioma per ús exclusiu per l'agenda.</em></p>"
            "<p><em>Recorda que tenim limitacions per afegir els idiomes.</em></p>"
            "<p><em>Les banderes no ens podem escollir, fem servir les de 'font awesome'.</p>"
            ),

            }
        )
    ]

class AlojamientoAdmin(TranslationAdmin, admin.ModelAdmin):
    filter_horizontal = ('tags',)
    inlines = [PostImagenInline, PostGaleriaImagenInline, PostFicheroImagenInline]

    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'metatitulo',
                'descripcion',
                'metadescripcion',
                'publicado',
                'tipo',
                'direccion',
                'telefono',
                'sitio_web',
                'capacidad',
                'horarios',
                'google_maps_link',
                'latitud',
                'longitud',
                'pet_friendly',
                'wifi',
                'adaptado_movilidad_reducida',
                'parking_gratis',
                'habitaciones_sin_humo',
                'servicio_habitaciones',
                'categoria',
                'tags'
            ],
            'description': (
                "<p><strong><em>Aquesta és l'administració d'un Allotjament.</em></strong></p>"
                "<p><em>Aquí pots introduir totes les dades relacionades amb el teu allotjament. "
                "Assegura't d'omplir tots els camps necessaris amb la informació correcta.</em></p>"
                "<p><em>Recorda que aquests camps estan destinats a recollir informació sobre l'allotjament, "
                "com el <strong>preu</strong>, els <strong>serveis</strong>, la <strong>capacitat</strong>, i altres detalls importants.</em></p>"
                "<p><em>Tingues en compte que la informació proporcionada ha de ser precisa per ajudar als visitants a fer la millor elecció possible.</em></p>"
                "<p><em>Si l'allotjament no té <strong>preu</strong>, pots deixar-lo a 0,00, i el sistema el detectarà com a gratuït.</em></p>"
                "<p><em>Assegura't d'afegir <strong>tags</strong> rellevants perquè seran utilitzats per millorar el <strong>SEO</strong> del teu allotjament.</em></p>"
                "<p><em>La informació com la <strong>latitud</strong> i <strong>longitud</strong> és crucial per a la funcionalitat de mapes, assegura't de proporcionar-la correctament.</em></p>"
            ),
            }
        )
    ]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(tipo="allotjament")
        return super(AlojamientoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



class RestauranteAdmin(TranslationAdmin, admin.ModelAdmin):
    filter_horizontal = ('tags',)
    inlines = [PostImagenInline, PostGaleriaImagenInline, PostFicheroImagenInline]

    fieldsets = [
        (None, {
            'fields': [
                'titulo',
                'metatitulo',
                'descripcion_corta',
                'descripcion',
                'metadescripcion',
                'publicado',
                'tipo',
                'direccion',
                'telefono',
                'sitio_web',
                'capacidad',
                'horarios',
                'google_maps_link',
                'latitud',
                'longitud',
                'pet_friendly',
                'opciones_vegetarianas',
                'wifi',
                'apto_para_celiacos',
                'terraza',
                'menu_infantil',
                'accessibilitat',
                'parking',
                'categoria',
                'tags'
            ],
            'description': (
                "<p><strong><em>Aquesta és l'administració d'un Restaurant.</em></strong></p>"
                "<p><em>Aquí pots introduir totes les dades relacionades amb el teu restaurant. "
                "Assegura't d'omplir tots els camps necessaris amb la informació correcta.</em></p>"
                "<p><em>Recorda que aquests camps estan destinats a recollir informació sobre el restaurant, "
                "com les <strong>opcions del menú</strong>, els <strong>serveis especials</strong>, i altres detalls importants.</em></p>"
                "<p><em>Tingues en compte que la informació proporcionada ha de ser precisa per ajudar als visitants a fer la millor elecció possible.</em></p>"
                "<p><em>Assegura't d'afegir <strong>tags</strong> rellevants perquè seran utilitzats per millorar el <strong>SEO</strong> del teu restaurant.</em></p>"
                "<p><em>La informació com la <strong>latitud</strong> i <strong>longitud</strong> és crucial per a la funcionalitat de mapes, assegura't de proporcionar-la correctament.</em></p>"
            ),
            }
        )
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(tipo="restaurant")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Restaurante, RestauranteAdmin)
admin.site.register(Alojamiento, AlojamientoAdmin)
admin.site.register(Idioma, IdiomaAdmin)
admin.site.register(Ruta, RutaAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(VisitaGuiada, VisitaGuidadaAdmin)
admin.site.register(CertificadoTurismoSostenible, CertificadoTurismoSostenibleAdmin)
admin.site.register(PlayListRuta, PlayListAdmin)