from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
import psycopg2
from psycopg2 import sql
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, jsonify
import requests
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
app.config['SECRET_KEY'] = 'efa8f62542204fb7a09e081699481658'  # Replace with your own secret key

# Database connection details
hostname = 'localhost'
database = 'demo'
username = 'postgres'
pwd = 'mamlesh'
port_id = 5432

def get_db_connection():
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    return conn

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        insert_script = sql.SQL('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)')
        cur.execute(insert_script, (username, email, password))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        print(f"Error during signup: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(sql.SQL('SELECT * FROM users WHERE email = %s AND password = %s'), (email, password))
        user = cur.fetchone()

        if user:
            token = jwt.encode({
                'user': email,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            update_script = sql.SQL('UPDATE users SET token = %s WHERE email = %s')
            cur.execute(update_script, (token, email))

            conn.commit()
            cur.close()
            conn.close()

            return jsonify({'token': token}), 200
        else:
            cur.close()
            conn.close()
            return jsonify({"message": "Invalid email or password"}), 401

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({'message': 'This is protected data'})



def get_btc_price():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?CMC_PRO_API_KEY=ad723eca-82b7-49f8-a5f5-2ff83836edc6"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for crypto in data['data']:
            if crypto['symbol'] == 'BTC':
                return crypto['quote']['USD']['price']
    return None

@app.route('/btc-price', methods=['GET'])
def btc_price():
    price = get_btc_price()
    if price is not None:
        return jsonify({"price": price}), 200
    else:
        return jsonify({"error": "Unable to fetch Bitcoin price"}), 500

@app.route('/submit-data', methods=['POST'])
def submit_data():
    data = request.json
    email = data.get('email')
    alert = data.get('alert')

    # Fetch the current BTC price
    btc_price = get_btc_price()
    message = "BTC price is not higher than the alert value."

    if btc_price is not None:
        alert_value = float(alert)
        if btc_price > alert_value:
            message = f"The current BTC price (${btc_price:.2f}) is higher than your alert value (${alert_value:.2f})."

            # Send email
            try:
                sender_email = "mamlesh.va06@gmail.com"
                receiver_email = email
                password = "nkdh bwyg seks qvni"

                # Create the email content
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = "BTC Price Alert"
                msg.attach(MIMEText(message, 'plain'))

                # Send the email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)
                server.quit()
                
                print("Email sent successfully")
            except Exception as e:
                print(f"Failed to send email: {e}")

        return jsonify({'message': 'Data received', 'btc_price': btc_price, 'comparison': message}), 200
    else:
        return jsonify({'message': 'Data received, but failed to fetch BTC price'}), 200
@app.route('/alerts/create/', methods=['POST'])
def create_alert():
    data = request.json
    email = data.get('email')
    alert_value = data.get('alert')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Insert the alert into the database
        insert_script = """
        INSERT INTO storage_alerts (email, alert_value) 
        VALUES (%s, %s)
        """
        cur.execute(insert_script, (email, alert_value))
        
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Alert created', 'alert': alert_value}), 201

    except Exception as e:
        print(f"Error creating alert: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/alerts/delete/', methods=['POST'])
def delete_alert():
    data = request.json
    email = data.get('email')

    # Here you would typically delete the alert from a database
    # For simplicity, we'll just return a success message
    return jsonify({'message': 'Alert deleted'}), 200


@app.route('/alerts/list/', methods=['GET'])
def list_alerts():
    email = request.args.get('email')
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch the alerts for the given email
        select_script = """
        SELECT alert_value, created_at
        FROM storage_alerts
        WHERE email = %s
        ORDER BY created_at DESC;
        """
        cur.execute(select_script, (email,))
        alerts = cur.fetchall()
        
        cur.close()
        conn.close()
        
        alert_list = [{'alert_value': alert[0], 'created_at': alert[1].strftime('%Y-%m-%d %H:%M:%S')} for alert in alerts]
        return jsonify({'alerts': alert_list}), 200
        
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
