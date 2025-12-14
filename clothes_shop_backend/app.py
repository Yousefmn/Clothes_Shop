from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date
from flask import Flask, request, jsonify
app = Flask(__name__)
CORS(app)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)



users = {
    "admin": "1234",
    "mustafa": "abcd"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


app.config['SQLALCHEMY_DATABASE_URI'] = (
    r'mssql+pyodbc://@3MoElJo\SQLEXPRESS/ClothesShopDB'
    '?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Supplier(db.Model):
    __tablename__ = 'Suppliers'
    SupplierID = db.Column(db.Integer, primary_key=True)
    SupplierName = db.Column(db.String(50))
    ContactName = db.Column(db.String(50))
    Phone = db.Column(db.String(20))
    Email = db.Column(db.String(50))

class Category(db.Model):
    __tablename__ = 'Categories'
    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(50))
    Description = db.Column(db.String(100))

class Customer(db.Model):
    __tablename__ = 'Customers'
    CustomerID = db.Column(db.Integer, primary_key=True)
    CustomerName = db.Column(db.String(50))
    Phone = db.Column(db.String(20))
    Email = db.Column(db.String(50))
    Address = db.Column(db.String(100))

class Product(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(50))
    SupplierID = db.Column(db.Integer)
    CategoryID = db.Column(db.Integer)
    Price = db.Column(db.Numeric(10,2))
    Quantity = db.Column(db.Integer)

class Order(db.Model):
    __tablename__ = 'Orders'
    OrderID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer)
    OrderDate = db.Column(db.Date)
    TotalAmount = db.Column(db.Numeric(10,2))

class OrderDetail(db.Model):
    __tablename__ = 'OrderDetails'
    OrderDetailID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer)
    ProductID = db.Column(db.Integer)
    Quantity = db.Column(db.Integer)
    Price = db.Column(db.Numeric(10,2))

class Employee(db.Model):
    __tablename__ = 'Employees'
    EmployeeID = db.Column(db.Integer, primary_key=True)
    EmployeeName = db.Column(db.String(50))
    Position = db.Column(db.String(50))
    Phone = db.Column(db.String(20))
    Email = db.Column(db.String(50))

class Inventory(db.Model):
    __tablename__ = 'Inventory'
    InventoryID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer)
    Quantity = db.Column(db.Integer)
    LastUpdated = db.Column(db.Date)

class Payment(db.Model):
    __tablename__ = 'Payments'
    PaymentID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer)
    PaymentDate = db.Column(db.Date)
    Amount = db.Column(db.Numeric(10,2))

class Shipper(db.Model):
    __tablename__ = 'Shippers'
    ShipperID = db.Column(db.Integer, primary_key=True)
    ShipperName = db.Column(db.String(50))
    Phone = db.Column(db.String(20))


@app.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        result = []
        for p in products:
            result.append({
                'ProductID': p.ProductID,
                'ProductName': p.ProductName,
                'SupplierID': p.SupplierID,
                'CategoryID': p.CategoryID,
                'Price': float(p.Price),
                'Quantity': p.Quantity
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(
        ProductName=data['ProductName'],
        SupplierID=data['SupplierID'],
        CategoryID=data['CategoryID'],
        Price=data['Price'],
        Quantity=data['Quantity']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully!'})

@app.route('/test-all-tables')
def test_all_tables():
    try:
        result = {
            "Suppliers": Supplier.query.count(),
            "Categories": Category.query.count(),
            "Customers": Customer.query.count(),
            "Products": Product.query.count(),
            "Orders": Order.query.count(),
            "OrderDetails": OrderDetail.query.count(),
            "Employees": Employee.query.count(),
            "Inventory": Inventory.query.count(),
            "Payments": Payment.query.count(),
            "Shippers": Shipper.query.count()
        }
        return jsonify({"message": "All tables are connected!", "counts": result})
    except Exception as e:
        return jsonify({"message": "DB connection failed", "error": str(e)})


@app.route('/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        result = []
        for o in orders:
            details = OrderDetail.query.filter_by(OrderID=o.OrderID).all()
            products_list = []
            for d in details:
                product = Product.query.get(d.ProductID)
                products_list.append({
                    "ProductID": product.ProductID,
                    "ProductName": product.ProductName,
                    "Quantity": d.Quantity,
                    "Price": float(d.Price)
                })
            result.append({
                "OrderID": o.OrderID,
                "CustomerID": o.CustomerID,
                "CustomerName": Customer.query.get(o.CustomerID).CustomerName,
                "TotalAmount": float(o.TotalAmount),
                "OrderDate": str(o.OrderDate),
                "Products": products_list
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"message": "Failed to fetch orders!", "error": str(e)}), 500




@app.route('/orders', methods=['POST'])
def add_order():
    try:
        data = request.json
        customer_id = data.get('CustomerID')
        product_id = data.get('ProductID')
        quantity = data.get('Quantity', 1)
        price = data.get('Price')

        if not all([customer_id, product_id, price]):
            return jsonify({'message': 'Missing data!'}), 400

        new_order = Order(
            CustomerID=customer_id,
            OrderDate=date.today(),
            TotalAmount=price * quantity
        )
        db.session.add(new_order)
        db.session.commit()

        order_detail = OrderDetail(
            OrderID=new_order.OrderID,
            ProductID=product_id,
            Quantity=quantity,
            Price=price
        )
        db.session.add(order_detail)
        db.session.commit()

        return jsonify({'message': 'Order added successfully!', 'OrderID': new_order.OrderID})
    except Exception as e:
        return jsonify({'message': 'Failed to add order!', 'error': str(e)}), 500


@app.route('/test-db')
def test_db():
    try:
        product = Product.query.first()
        if product:
            return jsonify({"message": "Database connected!", "first_product": product.ProductName})
        else:
            return jsonify({"message": "Database connected but no products yet!"})
    except Exception as e:
        return jsonify({"message": "DB connection failed", "error": str(e)})


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found!'}), 404
    data = request.json
    product.ProductName = data.get('ProductName', product.ProductName)
    product.SupplierID = data.get('SupplierID', product.SupplierID)
    product.CategoryID = data.get('CategoryID', product.CategoryID)
    product.Price = data.get('Price', product.Price)
    product.Quantity = data.get('Quantity', product.Quantity)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully!'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found!'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully!'})

@app.route('/')
def home():
    return jsonify({"message": "Backend is running successfully!"})


if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0', port=5000)


