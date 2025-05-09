class Product:
    def __init__(self, product_id, name, description, price, stock, image_url):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.image_url = image_url

    def update_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError("Not enough stock available")
        self.stock -= quantity

    def __str__(self):
        return f"{self.name} - ${self.price} (Stock: {self.stock})"

class Cart:
    def __init__(self):
        self.items = {}

    def add_to_cart(self, product, quantity):
        if product.product_id not in self.items:
            self.items[product.product_id] = {"product": product, "quantity": 0}
        if product.stock < quantity:
            raise ValueError("Not enough stock available")
        self.items[product.product_id]["quantity"] += quantity

    def remove_from_cart(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

    def calculate_total(self):
        return sum(item["product"].price * item["quantity"] for item in self.items.values())

    def checkout(self):
        for item in self.items.values():
            item["product"].update_stock(item["quantity"])
        self.items.clear()