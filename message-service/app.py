from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

messages = []

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
    return jsonify({'status': 'healthy', 'service': 'message-service'})

@app.route('/messages', methods=['GET'])
def get_messages():
    """Récupère tous les messages"""
    limit = request.args.get('limit', 50, type=int)
    return jsonify({'messages': messages[-limit:]})

@app.route('/messages', methods=['POST'])
def post_message():
    """Poste un nouveau message"""
    data = request.get_json()
    token = data.get('token', '')
    message = data.get('message', '')
    
    # Vérification du token
    auth_result = verify_token(token)
    if not auth_result or not auth_result.get('valid'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    username = auth_result.get('username')
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    new_message = {
        'id': len(messages) + 1,
        'username': username,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    messages.append(new_message)
    
    return jsonify(new_message), 201

@app.route('/messages/clear', methods=['DELETE'])
def clear_messages():
    """Efface tous les messages (pour les tests)"""
    messages.clear()
    return jsonify({'message': 'All messages cleared'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
