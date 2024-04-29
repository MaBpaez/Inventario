from django.contrib import admin
from .models import Producto


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cantidad', 'publicacion', 'creado', 'actualizado']
    prepopulated_fields = {'slug': ('nombre',)}

admin.site.register(Producto, ProductoAdmin)
