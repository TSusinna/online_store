from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure database and file upload settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

# Cart class
class Cart:
    def __init__(self):
        self.items = {}

    def add_to_cart(self, product, quantity):
        if product.id not in self.items:
            self.items[product.id] = {"product": product, "quantity": 0}
        if product.stock < quantity:
            raise ValueError("Not enough stock available")
        self.items[product.id]["quantity"] += quantity

    def remove_from_cart(self, product_id):
        if product_id in self.items:
            del self.items[product_id]

    def calculate_total(self):
        return sum(item["product"].price * item["quantity"] for item in self.items.values())

    def clear(self):
        self.items.clear()

# Initialize the database
with app.app_context():
    db.create_all()

# Initialize the cart
cart = Cart()

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def catalog():
    products = Product.query.all()
    return render_template('catalog.html', products=products)

@app.route('/cart', methods=['GET', 'POST'])
def view_cart():
    if request.method == 'POST':
        cart.clear()
        return redirect(url_for('catalog'))
    return render_template('cart.html', cart=cart)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form['quantity'])
    product = Product.query.get(product_id)
    if product:
        try:
            cart.add_to_cart(product, quantity)
        except ValueError as e:
            return str(e), 400
    return redirect(url_for('catalog'))

@app.route('/checkout', methods=['POST'])
def checkout():
    cart.clear()
    return redirect(url_for('catalog'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        image = request.files['image']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f"static/images/{filename}"

            new_product = Product(id=product_id, name=name, description=description, price=price, stock=stock, image_url=image_url)
            db.session.add(new_product)
            db.session.commit()

        return redirect(url_for('admin'))
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)