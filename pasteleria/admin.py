from django.contrib import admin
from .models import Linea, Producto

@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("Linea", "nombre", "descripcion", "imagen", "porciones", "aptocelíacos", "stock", "precio", "disponibleparaventa")
    list_filter = ("Linea", "aptocelíacos")
    search_fields = ("nombre",)

    def precio_form(self, obj):
        pass