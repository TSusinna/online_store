from flask import Flask, render_template, request, redirect, url_for
from models import Product, Cart

app = Flask(__name__)

# In-memory storage for products and cart
products = {
    1: Product(1, "Cigarette", "Just one cigarette, probably not used", 10.00, 10, "static/images/cigarette.jpg"),
    2: Product(2, "Trash bin", "May be full of loot", 800.00, 1, "static/images/trash_bin.png"),
    3: Product(3, "Guinea pig", "Not for eating", 500.00, 5, "static/images/guinea_pig.png"),
    4: Product(4, "Toilet", "Let's hope it doesn't have a head", 500.00, 500, "static/images/toilet.jpg")
}
cart = Cart()

@app.route('/')
def catalog():
    return render_template('catalog.html', products=products.values())

@app.route('/cart')
def view_cart():
    return render_template('cart.html', cart=cart)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form['quantity'])
    if product_id in products:
        try:
            cart.add_to_cart(products[product_id], quantity)
        except ValueError as e:
            return str(e), 400
    return redirect(url_for('catalog'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart.checkout()
    return redirect(url_for('catalog'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        image_url = request.form['image_url']
        products[product_id] = Product(product_id, name, description, price, stock, image_url)
        return redirect(url_for('admin'))
    return render_template('admin.html', products=products.values())

if __name__ == '__main__':
    app.run(debug=True)