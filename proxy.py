from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
DEEPSEEK_API = "https://api.deepseek.com/v1"
API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.route('/v1/chat/completions', methods=['POST'])
def proxy():
    try:
        # Получаем и модифицируем запрос
        payload = request.json
        payload["safe_mode"] = False  # Отключаем фильтрацию
        
        # Отправляем в DeepSeek
        response = requests.post(
            f"{DEEPSEEK_API}/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        
        # Возвращаем ответ Janitor AI
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({
            "error": "Janitor Proxy Error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
