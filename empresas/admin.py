from django.contrib import admin
from django.utils.html import format_html


from .models import Empresas, Internos, Actas, Rectificaciones, Desinfeccion  


@admin.register(Empresas)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('empresa',)  

@admin.register(Internos)
class InternoAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'numero_interno', 'chapa_mop')
    list_filter = ('empresa__empresa', 'numero_interno')
   

@admin.register(Actas)
class ActasAdmin(admin.ModelAdmin):
    list_display = ('numero_de_acta', 'fecha', 'empresa', 'interno', 'descripcion', 'horas_intimacion', 'acta_pdf_link')
    list_display_links = ('numero_de_acta',)  # Corrected to 'numero_de_acta'
    list_filter = ('numero_de_acta', 'empresa__empresa', 'interno')  # Corrected to 'numero_de_acta'
    search_fields = ('numero_de_acta', 'empresa__empresa', 'interno')  # Corrected to 'numero_de_acta'

    def acta_pdf_link(self, obj):
        if obj.acta_pdf:
            return format_html('<a href="{}" target="_blank">Ver PDF</a>', obj.acta_pdf.url)
        return "N/A"
    acta_pdf_link.short_description = 'PDF'

@admin.register(Rectificaciones)  # Corrected model name
class RectificacionesAdmin(admin.ModelAdmin):
    list_display = ('numero_rectificacion', 'fecha', 'empresa', 'interno', 'numero_acta', 'rectificacion_pdf_link')
    list_filter = ('numero_rectificacion', 'empresa__empresa', 'interno')  # Corrected to 'numero_de_acta'
    search_fields = ('numero_rectificacion', 'empresa__empresa', 'interno') # Corrected to 'numero_de_acta'

    def rectificacion_pdf_link(self, obj):
        if obj.rectificacion_pdf:
            return format_html('<a href="{}" target="_blank">Ver PDF</a>', obj.rectificacion_pdf.url)
        return "N/A"
    rectificacion_pdf_link.short_description = 'PDF'
 

@admin.register(Desinfeccion)
class DesinfeccionAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'numero_interno', 'chapa_mop', 'fecha_realizacion', 'fecha_vencimiento', 'desinfeccion_pdf_link')
    list_filter = ('empresa__empresa', 'numero_interno')
    search_fields = ('empresa__empresa', 'numero_interno')

    def desinfeccion_pdf_link(self, obj):
        if obj.desinfeccion_pdf:
            return format_html('<a href="{}" target="_blank">Ver PDF</a>', obj.desinfeccion_pdf.url)
        return "N/A"
    desinfeccion_pdf_link.short_description = 'PDF'


