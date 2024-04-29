from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # ruta que maneja específicamente la URL /productos/. Cuando se conecta a esta URL,
    # se crea una instancia de ProductosListado con page establecido en 1
    re_path(
        r"ws/productos/$", consumers.ProductosListado.as_asgi(), kwargs={'page': 1}
    ),
    re_path(r"ws/productos/(?P<page>\d+)/$", consumers.ProductosListado.as_asgi()),
    re_path(
        r"ws/productos/(?P<nombre_producto>[\w-]+)/$",
        consumers.UnidadesProducto.as_asgi(),
    ),
]
