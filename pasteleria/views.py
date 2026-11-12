from django.shortcuts import render

from .models import Producto


def catalogo(request):
    productos = Producto.objects.filter(
        disponibleparaventa=True
    ).select_related('Linea').only(
        'id', 'nombre', 'imagen', 'precio', 'Linea__nombre'
    ).order_by('nombre')
    return render(request, 'index.html', {'productos': productos})
