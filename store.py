from models import Cart

class Store:
    def __init__(self, admin):
        self.admin = admin
        self.cart = Cart()

    def browse_products(self):
        for product in self.admin.products.values():
            print(product)

    def add_to_cart(self, product_id, quantity):
        if product_id not in self.admin.products:
            raise ValueError("Product not found.")
        product = self.admin.products[product_id]
        self.cart.add_to_cart(product, quantity)

    def checkout(self):
        total = self.cart.calculate_total()
        print(f"Total: ${total}")
        self.cart.checkout()
        print("Purchase successful!")