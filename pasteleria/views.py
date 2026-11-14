from django.shortcuts import render

from .models import Linea, Producto


def catalogo(request):
    nombre = request.GET.get('nombre', '').strip()
    linea_id = request.GET.get('linea', '').strip()
    productos = Producto.objects.filter(
        disponibleparaventa=True
    )
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if linea_id:
        if linea_id.isdecimal():
            productos = productos.filter(Linea_id=int(linea_id))
        else:
            productos = productos.none()
    productos = productos.select_related('Linea').only(
        'id', 'nombre', 'imagen', 'precio', 'Linea__nombre'
    ).order_by('nombre')
    lineas = Linea.objects.order_by('nombre')
    return render(request, 'index.html', {
        'productos': productos,
        'lineas': lineas,
        'nombre_buscado': nombre,
        'linea_seleccionada': linea_id,
        'filtros_aplicados': bool(nombre or linea_id),
    })
