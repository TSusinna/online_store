from admin import Admin
from store import Store

def main():
    admin = Admin()

    # Admin adds products
    admin.add_product(1, "Laptop", "High-performance laptop", 1200.00, 10, "laptop.jpg")
    admin.add_product(2, "Phone", "Latest smartphone", 800.00, 20, "phone.jpg")

    store = Store(admin)

    # User browses products
    print("Available Products:")
    store.browse_products()

    # User adds products to cart
    store.add_to_cart(1, 1)
    store.add_to_cart(2, 2)

    # Checkout
    print("\nChecking out...")
    store.checkout()

    # Admin updates stock
    print("\nAdmin updates stock:")
    admin.update_product_stock(1, 15)
    admin.list_products()

if __name__ == "__main__":
    main()