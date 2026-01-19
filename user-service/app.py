from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Utilisateurs connectés (stockage en mémoire)
connected_users = {}

AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://auth-service:5000')

def verify_token(token):
    """Vérifie le token via le service d'authentification"""
    try:
        response = requests.post(f'{AUTH_SERVICE_URL}/verify', json={'token': token})
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'user-service'})

@app.route('/users/online', methods=['GET'])
def get_online_users():
    """Récupère la liste des utilisateurs en ligne"""
    return jsonify({'users': list(connected_users.keys())})

@app.route('/users/connect', methods=['POST'])
def connect_user():
    """Marque un utilisateur comme connecté"""
    data = request.get_json()
    token = data.get('token', '')
    
    # Vérification du token
    auth_result = verify_token(token)
    if not auth_result or not auth_result.get('valid'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    username = auth_result.get('username')
    connected_users[username] = {
        'connected_at': datetime.utcnow().isoformat(),
        'last_seen': datetime.utcnow().isoformat()
    }
    
    return jsonify({
        'username': username,
        'status': 'connected'
    })

@app.route('/users/disconnect', methods=['POST'])
def disconnect_user():
    """Déconnecte un utilisateur"""
    data = request.get_json()
    token = data.get('token', '')
    
    # Vérification du token
    auth_result = verify_token(token)
    if not auth_result or not auth_result.get('valid'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    username = auth_result.get('username')
    if username in connected_users:
        del connected_users[username]
    
    return jsonify({
        'username': username,
        'status': 'disconnected'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
