import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class UnidadesProducto(WebsocketConsumer):
    '''Consumer sincrónico'''

    def connect(self):
        print(self.scope)
        print(self.scope['url_route']['kwargs']['nombre_producto'])

        self.nombre_producto = self.scope['url_route']['kwargs']['nombre_producto']
        self.product_group_name = f'producto_{self.nombre_producto}'

        async_to_sync(self.channel_layer.group_add)(
            self.product_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Abandonar el grupo product
        async_to_sync(self.channel_layer.group_discard)(
            self.product_group_name, self.channel_name
        )

    # Recibir mensaje desde el websocket
    # Para actualizar las cantidades del producto en tiempo real, necesitarás manejar los
    # mensajes recibidos en el WebSocket. En nuestro caso como desde el cliente
    # websocket no vamos a enviar ningún mensaje al servidor websocket, este método no
    # es necesario.

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Enviar mensaje al grupo product
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.product_group_name, {'type': 'producto_message', 'message': message}
    #     )

    # Recibir mensaje desde el grupo product
    def producto_message(self, event):
        message = event['message']

        # Enviar mensaje al websocket(cliente)
        self.send(text_data=json.dumps({'message': message}))


class ProductosListado(WebsocketConsumer):
    '''Consumer sincrónico para el listado de productos'''

    def connect(self):
        print('ProductosListado')
        self.page = self.scope['url_route']['kwargs']['page']
        self.product_list_group_name = f'product_list_{self.page}'

        async_to_sync(self.channel_layer.group_add)(
            self.product_list_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Abandona el grupo product list
        async_to_sync(self.channel_layer.group_discard)(
            self.product_list_group_name, self.channel_name
        )

    # Recibir mensaje desde el grupo product list
    def product_list_message(self, event):
        message = event['message']
        producto_id = event['producto_id']

        # Enviar mensaje al WebSocket(cliente)
        self.send(text_data=json.dumps({'producto_id': producto_id,'message': message}))

