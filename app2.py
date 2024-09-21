from flask import Flask,render_template, request, jsonify
import sqlite3
import math

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    print("hi")
    return render_template('mainpage.html')

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('delivery_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Utility function to calculate distance between two geo points (Haversine formula)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Add a customer
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO Customer (first_name, last_name, email, phone_number, address) VALUES (?, ?, ?, ?, ?)', 
                 (data['first_name'], data['last_name'], data['email'], data['phone_number'], data['address']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Customer added successfully!'})

# Add a delivery person
@app.route('/delivery_person', methods=['POST'])
def add_delivery_person():
    data = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO DeliveryPerson (first_name, last_name, phone_number, vehicle_type, current_latitude, current_longitude) VALUES (?, ?, ?, ?, ?, ?)', 
                 (data['first_name'], data['last_name'], data['phone_number'], data['vehicle_type'], data['current_latitude'], data['current_longitude']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Delivery person added successfully!'})

# Create an order
@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO Orders (customer_id, delivery_address, total_amount, delivery_latitude, delivery_longitude) VALUES (?, ?, ?, ?, ?)', 
                 (data['customer_id'], data['delivery_address'], data['total_amount'], data['delivery_latitude'], data['delivery_longitude']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Order created successfully!'})

# Assign a nearby delivery person to an order
@app.route('/assign_delivery', methods=['POST'])
def assign_delivery():
    data = request.json
    order_id = data['order_id']

    # Get order location
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM Orders WHERE order_id = ?', (order_id,)).fetchone()
    
    if not order:
        return jsonify({'error': 'Order not found'})

    order_lat = order['delivery_latitude']
    order_lon = order['delivery_longitude']

    # Find nearest available delivery person
    delivery_persons = conn.execute('SELECT * FROM DeliveryPerson WHERE available = 1').fetchall()
    
    nearest_person = None
    min_distance = float('inf')

    for person in delivery_persons:
        distance = calculate_distance(order_lat, order_lon, person['current_latitude'], person['current_longitude'])
        if distance < min_distance:
            min_distance = distance
            nearest_person = person
    
    if nearest_person:
        # Assign the delivery person
        conn.execute('UPDATE Orders SET delivery_person_id = ? WHERE order_id = ?', (nearest_person['delivery_person_id'], order_id))
        conn.execute('UPDATE DeliveryPerson SET available = 0 WHERE delivery_person_id = ?', (nearest_person['delivery_person_id'],))
        conn.commit()
        conn.close()
        return jsonify({'message': f'Delivery person {nearest_person["first_name"]} assigned to order {order_id}'})
    else:
        return jsonify({'message': 'No delivery person available'})

# Update order status
@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    data = request.json
    order_id = data['order_id']
    order_status = data['order_status']

    conn = get_db_connection()
    conn.execute('UPDATE Orders SET order_status = ? WHERE order_id = ?', (order_status, order_id))
    conn.commit()
    conn.close()
    return jsonify({'message': f'Order {order_id} status updated to {order_status}'})
def get_db_connection():
    conn = sqlite3.connect('delivery_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for the login page (GET request renders login form, POST request handles login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()

        if user:
            # Create session for the user
            session['user_id'] = user['user_id']
            session['email'] = user['email']
            return redirect(url_for('main_page'))
        else:
            return "Invalid email or password, please try again", 401
    
    return render_template('login.html')

if __name__== '__main__':
    app.run(debug=True)
