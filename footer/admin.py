from django.contrib import admin
from .models import Footer, FooterEmpresa, FooterInformacion

class FooterEmpresaInline(admin.StackedInline):
    model = FooterEmpresa
    extra = 1
    # Define cómo se presentan los campos en el administrador
    fieldsets = (
        (None, {  # None significa que no hay título para este fieldset
            'fields': ('titulo', 'imagen', 'enlace','footer'),
            'description': (
                "<p><strong>Configuració de les empreses en el footer:</strong></p>"
                "<p>Aquí pots gestionar les empreses que apareixen en el footer. "
                "Inclou un <strong>títol</strong> per a l'empresa, "
                "puja una <strong>imatge</strong> que segueixi les recomanacions de dimensions (143 x 72 px), "
                "i, si es vol, afegeix un <strong>enllaç</strong> al lloc web de l'empresa.</p>"
                "<p>És important seleccionar correctament el <strong>footer associat</strong> "
                "per assegurar que l'empresa aparegui en la secció correcta del lloc web.</p>"
            ),
        }),
    )

class FooterInformacionInline(admin.StackedInline):
    model = FooterInformacion
    extra = 1

    fieldsets = (
        (None, {  # None significa que no hay título para este fieldset
            'fields': ('imagen', 'direccion', 'telefono', 'correo_contacto', 'paginas_legales'),
            'description': (
                "<p><strong>Configuració de la informació de contacte i legal del footer:</strong></p>"
                "<p>Aquesta secció permet gestionar la informació de contacte que es mostra al footer de totes les pàgines. "
                "Inclou una <strong>imatge</strong> que serà rellevant per al context del footer, "
                "la <strong>direcció</strong> física de l'entitat o empresa, un <strong>telèfon</strong> de contacte, "
                "i un <strong>correu electrònic</strong> per facilitar la comunicació amb els visitants del lloc web.</p>"
                "<p>A més, pots vincular <strong>pàgines legals</strong> específiques que es considerin importants "
                "per a la transparència i el compliment normatiu. Aquestes pàgines poden incloure termes i condicions, "
                "polítiques de privacitat, avís legal, entre altres.</p>"
                "<p>És crucial que la informació proporcionada sigui precisa i estigui actualitzada "
                "per assegurar que els usuaris tenen accés a dades de contacte fiables i comprenen les polítiques "
                "que regeixen l'ús del lloc web.</p>"
            ),
        }),
    )

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    inlines = [FooterEmpresaInline, FooterInformacionInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'description'),
            'description': (
                "<p><strong>Configuració General del Footer:</strong></p>"
                "<p>Aquesta secció permet personalitzar el títol i la descripció que apareixen en el footer de totes les pàgines del lloc web. "
                "El footer és un element clau per a la navegació i proporciona informació important als visitants. "
                "Assegura't que el títol i la descripció siguin breus i concisos, oferint una visió general efectiva.</p>"
                "<p>A més, a través dels elements inline, podràs gestionar la informació específica d'empreses destacades "
                "i la informació de contacte i legal relacionada, directament des d'aquesta interfície, facilitant una administració "
                "centralitzada del contingut del footer. Cada secció inline inclou instruccions detallades per garantir "
                "una configuració adequada i coherent.</p>"
                "<p>La correcta configuració i actualització del footer és fonamental per mantenir una comunicació efectiva "
                "i transparent amb els usuaris del lloc web, assegurant que tenen accés fàcil a la informació de contacte, "
                "pàgines legals, i altres recursos importants.</p>"
            ),
        }),
    )