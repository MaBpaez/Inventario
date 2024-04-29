from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, unique_for_date="publicacion")
    descripcion = models.TextField(blank=True)
    cantidad = models.IntegerField()
    publicacion = models.DateTimeField("fecha de publicación", default=timezone.now)
    creado = models.DateTimeField("fecha de creación", auto_now_add=True)
    actualizado = models.DateTimeField("fecha de modificación", auto_now=True)

    def get_absolute_url(self):
        return reverse(
            "inventario:detalle-inventario",
            args=[self.slug],
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        object_list = Producto.objects.all()
        paginator = Paginator(object_list, 3)
        total_pages = paginator.num_pages

        channel_layer = get_channel_layer()

        # Enviar un mensaje al grupo del producto individual
        async_to_sync(channel_layer.group_send)(
            f'producto_{self.slug}',
            {'type': 'producto_message', 'message': self.cantidad},
        )

        # Enviar un mensaje a cada grupo de la lista de productos
        # num_pages es una propiedad de Paginator que te da el número total de páginas
        for page in range(1, total_pages + 1):
            async_to_sync(channel_layer.group_send)(
                f'product_list_{page}',
                {'type': 'product_list_message', 'producto_id': self.id,'message': self.cantidad},
            )

    def __str__(self):
        return self.nombre
