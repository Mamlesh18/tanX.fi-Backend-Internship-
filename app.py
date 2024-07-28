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



if __name__ == '__main__':
    app.run(debug=True)
