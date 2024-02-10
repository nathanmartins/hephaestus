import re
from flask import Flask, request, jsonify
import jwt
import datetime

SECRET_KEY = 'super-secret-key'

app = Flask(__name__)

# Hardcoded credentials (for demonstration purposes)
VALID_CREDENTIALS = {
    'email': 'pierre@palenca.com',
    'password': 'MyPwdChingon123'
}


@app.route('/')
def hello():
    return 'Hello Palenca'


@app.route('/uber/login', methods=['POST'])
def uber_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Email validation using regular expression
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        response = {
            'message': 'INVALID_EMAIL_FORMAT',
            'details': 'Please provide a valid email address'
        }
        return jsonify(response), 400

    # Password validation
    if not isinstance(password, str) or len(password) < 6:
        response = {
            'message': 'INVALID_PASSWORD',
            'details': 'Password must be a string with over 5 characters'
        }
        return jsonify(response), 400

    # Authenticate user
    if email == VALID_CREDENTIALS['email'] and password == VALID_CREDENTIALS['password']:
        # Create JWT token
        access_token = jwt.encode(
            {'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            SECRET_KEY
        )
        response = {
            'message': 'SUCCESS',
            'access_token': access_token
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'CREDENTIALS_INVALID',
            'details': 'Incorrect username or password'
        }
        return jsonify(response), 401


@app.route('/uber/profile/<access_token>', methods=['GET'])
def uber_profile(access_token):
    try:
        # Decode JWT token to retrieve email
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
        email = payload['email']

        # Check if the email matches the valid credentials
        if email == VALID_CREDENTIALS['email']:
            # Assuming you have some profile data to return
            profile_data = {
                'name': 'Pierre',
                'email': email,
                'age': 30
                # Add more profile data as needed
            }
            response = {
                'message': 'SUCCESS',
                'platform': 'uber',
                'profile': profile_data
            }
            return jsonify(response), 200
        else:
            response = {
                'message': 'CREDENTIALS_INVALID',
                'details': 'Incorrect token'
            }
            return jsonify(response), 401
    except jwt.ExpiredSignatureError:
        response = {
            'message': 'TOKEN_EXPIRED',
            'details': 'Token has expired'
        }
        return jsonify(response), 401
    except jwt.InvalidTokenError:
        response = {
            'message': 'INVALID_TOKEN',
            'details': 'Invalid token provided'
        }
        return jsonify(response), 401


if __name__ == '__main__':
    app.run(debug=True, port=8000)
