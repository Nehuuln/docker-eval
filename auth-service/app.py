from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.environ.get('SECRET_KEY', 'secret-key-dev')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'auth-service'})

@app.route('/login', methods=['POST'])
def login():
    """Génère un token JWT pour un utilisateur"""
    data = request.get_json()
    username = data.get('username', '')
    
    if not username:
        return jsonify({'error': 'Username required'}), 400
    
    # Génération simple d'un token JWT
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'token': token,
        'username': username
    })

@app.route('/verify', methods=['POST'])
def verify():
    """Vérifie la validité d'un token JWT"""
    data = request.get_json()
    token = data.get('token', '')
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({
            'valid': True,
            'username': payload['username']
        })
    except jwt.ExpiredSignatureError:
        return jsonify({'valid': False, 'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'valid': False, 'error': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
