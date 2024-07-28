from flask import Flask, request, jsonify, make_response, render_template, session, flash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from pytz import utc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'efa8f62542204fb7a09e081699481658'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    if not session.get('logged_in') or 'expiration' not in session or utc.localize(datetime.utcnow()) > session['expiration']:
        session.clear()
        return render_template('login.html')
    else:
        return 'logged in currently'

@app.route('/public')
def public():
    return 'For Public'

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard!'

@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        session['expiration'] = utc.localize(datetime.utcnow() + timedelta(minutes=1))

        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(utc.localize(datetime.utcnow() + timedelta(seconds=60)))
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return 'Logged out successfully'

if __name__ == "__main__":
    app.run(debug=True)
