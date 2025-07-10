# app.py - обновленная версия
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DEEPSEEK_API = "https://api.deepseek.com/v1"
API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Правильные модели DeepSeek
DEEPSEEK_MODELS = {
    "deepseek-chat": "deepseek-chat",
    "deepseek-coder": "deepseek-coder"
}

@app.route('/v1/chat/completions', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        payload = request.json
        
        # 1. Фикс модели
        if 'model' in payload:
            # Преобразуем модель Janitor AI в модель DeepSeek
            if payload['model'] in DEEPSEEK_MODELS:
                payload['model'] = DEEPSEEK_MODELS[payload['model']]
            else:
                # По умолчанию используем deepseek-chat
                payload['model'] = "deepseek-chat"
        else:
            # Если модель не указана - устанавливаем deepseek-chat
            payload['model'] = "deepseek-chat"
        
        # 2. Отключаем безопасный режим
        payload["safe_mode"] = False
        
        # 3. Отправляем запрос в DeepSeek
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{DEEPSEEK_API}/chat/completions",
            headers=headers,
            json=payload
        )
        
        return _corsify_actual_response(jsonify(response.json())), response.status_code

    except Exception as e:
        return _corsify_actual_response(jsonify({
            "error": "Proxy error",
            "message": str(e)
        })), 500

def _build_cors_preflight_response():
    response = jsonify({"message": "Preflight"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
