# 📁 Файл: janitor_proxy.py
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
DEEPSEEK_API = "https://api.deepseek.com/v1"

# 🔑 Ваш API-ключ DeepSeek (установите в переменных окружения Render)
API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.route('/v1/chat/completions', methods=['POST'])
def proxy():
    try:
        # ⚙️ Получаем данные от Janitor AI
        payload = request.json
        
        # 🔓 Принудительно отключаем безопасный режим
        if payload.get("model") == "deepseek-chat":
            payload["safe_mode"] = False
        
        # 🔄 Отправляем запрос в DeepSeek с вашим ключом
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{DEEPSEEK_API}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # 📤 Возвращаем ответ в Janitor AI
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({"error": f"Proxy error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)