from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.inventario, name='inventario'),
    path('<slug:nombre_producto>/', views.detalle_inventario, name='detalle-inventario'),
]
