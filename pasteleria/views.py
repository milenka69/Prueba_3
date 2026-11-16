from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db import transaction
from django.views.decorators.http import require_safe

from .forms import EncargoForm
from .models import Encargos, Linea, Producto


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
        'id', 'nombre', 'imagen', 'stock', 'precio', 'Linea__nombre'
    ).order_by('nombre')
    lineas = Linea.objects.order_by('nombre')
    return render(request, 'index.html', {
        'productos': productos,
        'lineas': lineas,
        'nombre_buscado': nombre,
        'linea_seleccionada': linea_id,
        'filtros_aplicados': bool(nombre or linea_id),
    })

def detalle(request, producto_id):
    producto = get_object_or_404(
        Producto, id=producto_id, disponibleparaventa=True
    )
    return render(request, 'detalle.html', {'producto': producto})


def encargar(request, producto_id):
    producto = get_object_or_404(
        Producto,
        id=producto_id,
        disponibleparaventa=True
    )
    form = EncargoForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
        cantidad = form.cleaned_data['unidadesApedir']

        with transaction.atomic():
            producto = get_object_or_404(
                Producto.objects.select_for_update(), 
                id=producto_id, 
                disponibleparaventa=True
                )

            if cantidad > producto.stock:
                form.add_error('unidadesApedir', f'La cantidad solicitada excede el stock disponible. Quedan {producto.stock} unidades en stock.')

            else:
                encargo = form.save(commit=False)
                encargo.producto = producto
                encargo.fechapedido = timezone.localdate()
                encargo.total = producto.precio * cantidad
                encargo.save()

                producto.stock -= cantidad
                producto.save()

                messages.success(request, 'Tu encargo fue registrado correctamente.')
                return redirect('comprobante', encargo_id=encargo.pk)

    return render(request, 'encargo.html', {
        'producto': producto,
        'form': form
    })


@require_safe
def comprobante(request, encargo_id):
    encargo = get_object_or_404(
        Encargos.objects.select_related('producto'), pk=encargo_id
    )
    total = encargo.total
    if total is None:
        total = encargo.producto.precio * encargo.unidadesApedir
    return render(request, 'comprobante.html', {'encargo': encargo, 'total': total})
