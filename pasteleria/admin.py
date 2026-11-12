from django.contrib import admin
from .models import Linea, Producto, Encargos

@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("Linea", "nombre", "descripcion", "imagen", "porciones", "aptoceliacos", "stock", "precio_form", "disponibleparaventa")
    list_filter = ("Linea", "aptoceliacos")
    search_fields = ("nombre",)

    def precio_form(self, obj):
        return f"${obj.precio: ,}".replace("," , ".")

admin.site.register(Encargos)