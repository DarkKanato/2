from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.client.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

# CRUD операции для Client

def create_client(name, email, phone_number, address):
    client = Client(name=name, email=email, phone_number=phone_number, address=address)
    client.save()
    return client

def get_client(client_id):
    return Client.objects.get(id=client_id)

def update_client(client_id, name=None, email=None, phone_number=None, address=None):
    client = Client.objects.get(id=client_id)
    if name:
        client.name = name
    if email:
        client.email = email
    if phone_number:
        client.phone_number = phone_number
    if address:
        client.address = address
    client.save()
    return client

def delete_client(client_id):
    client = Client.objects.get(id=client_id)
    client.delete()

# CRUD операции для Product

def create_product(name, description, price, quantity):
    product = Product(name=name, description=description, price=price, quantity=quantity)
    product.save()
    return product

def get_product(product_id):
    return Product.objects.get(id=product_id)

def update_product(product_id, name=None, description=None, price=None, quantity=None):
    product = Product.objects.get(id=product_id)
    if name:
        product.name = name
    if description:
        product.description = description
    if price:
        product.price = price
    if quantity:
        product.quantity = quantity
    product.save()
    return product

def delete_product(product_id):
    product = Product.objects.get(id=product_id)
    product.delete()

# CRUD операции для Order

def create_order(client_id, product_quantities):
    order = Order(client_id=client_id)
    order.save()
    total_amount = 0
    for product_id, quantity in product_quantities.items():
        product = Product.objects.get(id=product_id)
        order_item = OrderItem(order=order, product=product, quantity=quantity, price=product.price)
        order_item.save()
        total_amount += product.price * quantity
    order.total_amount = total_amount
    order.save()
    return order

def get_order(order_id):
    return Order.objects.select_related('client').prefetch_related('orderitem_set__product').get(id=order_id)

def update_order(order_id, client_id=None, product_quantities=None):
    order = Order.objects.get(id=order_id)
    if client_id:
        order.client_id = client_id
    if product_quantities:
        order.orderitem_set.all().delete()
        total_amount = 0
        for product_id, quantity in product_quantities.items():
            product = Product.objects.get(id=product_id)
            order_item = OrderItem(order=order, product=product, quantity=quantity, price=product.price)
            order_item.save()
            total_amount += product.price * quantity
        order.total_amount = total_amount
    order.save()
    return order

def delete_order(order_id):
    order = Order.objects.get(id=order_id)
    order.delete()

