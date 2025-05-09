from models import Product

class Admin:
    def __init__(self):
        self.products = {}

    def add_product(self, product_id, name, description, price, stock, image_url):
        if product_id in self.products:
            raise ValueError("Product ID already exists.")
        self.products[product_id] = Product(product_id, name, description, price, stock, image_url)

    def update_product_stock(self, product_id, new_stock):
        if product_id not in self.products:
            raise ValueError("Product not found.")
        self.products[product_id].stock = new_stock

    def list_products(self):
        for product in self.products.values():
            print(product)