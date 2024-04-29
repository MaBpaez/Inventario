from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Producto


def inventario(request):
    object_list = Producto.objects.all()

    paginator = Paginator(object_list, 3)  # (objects) en cada página
    page = request.GET.get("page")

    try:
        productos_inventario = paginator.page(page)  # todos los productos de una página

    except PageNotAnInteger:
        productos_inventario = paginator.page(1)

    except EmptyPage:
        productos_inventario = paginator.page(paginator.num_pages)

    return render(
        request, 'inventario/list.html', {'productos_inventario': productos_inventario}
    )


def detalle_inventario(request, nombre_producto):
    producto = get_object_or_404(Producto, slug=nombre_producto)

    return render(request, 'inventario/detalle.html', {'producto': producto})
