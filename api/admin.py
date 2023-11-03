from django.contrib import admin
from .models import Teenvio, Subscriptor, MailManager, GmailServer, OutlookServer
from django.http import HttpResponse
import csv
# Register your models here.

class GamilServerInline(admin.TabularInline):  # You can also use 'admin.StackedInline' for a different display style
    model = GmailServer
    max_num = 1

class OutlookServerInline(admin.TabularInline):
    model = OutlookServer
    max_num = 1

@admin.register(MailManager)
class MailManagerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'mail_server',
            ],
            'description': (
                "<p><strong><em>Aquesta és l'administració de la configuració del correu.</em></strong></p>"
                "<p><em>Pots triar entre GMAIL o OUTLOOK com a servidor de correu. </em></p>"
                "<p><em>S'ha d'activar l'ús d'aplicacions no segures en el compte de Gmail que vols fer servir com a servidor.</em><strong>https://myaccount.google.com/lesssecureapps</strong></p>"
                "<p><em>Si surt error quan fen l'enviament de correu amb GMAIL, pot ser que la opció 'ús' d'aplicacions no segures estigui desactivada. </em></p>"
                "<p><em>L'ús del servidor de GMAIL és a la configuració de config.json, si es vol modificar el servidor en profunditat.</em></p>"
                "<p><em>Si es vol afefir un altre servidor alternatiu, primer s'ha de programar i afegir-ho a la vista</em></p>"
            )
        })
    ]

    # Define save_model method to handle uniqueness validation and updating
    def save_model(self, request, obj, form, change):
        # Ensure only one instance of MailManager exists
        if not MailManager.objects.exists():
            super().save_model(request, obj, form, change)
        else:
            obj.pk = MailManager.objects.first().pk  # Update the existing instance instead of creating a new one
            super().save_model(request, obj, form, change)
    

    inlines = [GamilServerInline, OutlookServerInline]





@admin.register(Teenvio)
class TeenvioAdmin(admin.ModelAdmin):
    list_display = ['gid', 'user', 'plan']

    fieldsets = [
        (None, {
            'fields': [
                'gid',
                'user',
                'password',
                'plan',
                'url',
                'action'
                ],

            'description': (
                "<p><strong><em>Aquesta és l'administració de Teenvio.</em></strong></p>"
                "<p><em>En aquesta secció, pots gestionar l'API del teu usuari de Teenvío.</em></p>"
                "<p><em>Assegura't d'omplir tots els camps.</em></p>"
                "<p><em>Només pots tenir una instància d'aquest model.</em></p>"
                "<p><em>Enllaç d'accés cap Teenvio: <a href='https://app.teenvio.com/v4/public/login/' target='_blank'>https://app.teenvio.com/v4/public/login/</a>.</em></p>"
            ),
        }),
        # Resto de los fieldsets
    ]




@admin.register(Subscriptor)
class SubscriptorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']  # Mostrar campos en la lista del admin


    fieldsets = [
        (None, {
            'fields': [
                'name',
                'email',
                'exportable',
                'sincronizado',
                'created_at'
                ],

            'description': (
                "<p><strong><em>Aquesta és l'administració dels subscriptors.</em></strong></p>"
                "<p><em>En aquesta secció, pots gestionar els subscriptors que s'han donat d'alta pel formulari de la web.</em></p>"
                "<p><em>Assegura't de no repetir els subscriptors.</em></p>"
                "<p><em>Pots tornar a sincronitzar els subscriptors amb Teenvio.</em></p>"
                "<p><em>Pots seleccionar els subscriptors que vols per una sincronització parcial.</em></p>"
            ),
        }),
        # Resto de los fieldsets
    ]


    def formatted_email(self, obj):
        return f'\t{obj.email}'  # Agrega una tabulación al inicio del correo electrónico
    

    def export_unsynced_subscribers_to_csv(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="unsynced_subscribers.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Fecha de creación'])

        unsynced_subscribers = queryset.filter(sincronizado=False)

        for subscriber in unsynced_subscribers:
            writer.writerow([subscriber.name, subscriber.email, subscriber.created_at])
        
        return response

    export_unsynced_subscribers_to_csv.short_description = 'Exportar subcriptores no sincronizados a CSV'



    def export_subscribers_to_csv(modeladmin,request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Fecha de creación'])  # Encabezados de las columnas
        
        for subscriber in queryset:
            if subscriber.exportable:
                writer.writerow([subscriber.name, subscriber.email, subscriber.created_at])
        return response
    export_subscribers_to_csv.short_description = 'Exporta els subcriptors seleccionats a CSV'

    actions = [export_subscribers_to_csv, export_unsynced_subscribers_to_csv] # Agregar la acción personalizada



