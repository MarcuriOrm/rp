from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
DEEPSEEK_API = "https://api.deepseek.com/v1"
API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.route('/v1/chat/completions', methods=['POST'])
def proxy():
    try:
        payload = request.json
        if payload.get("model") == "deepseek-chat":
            payload["safe_mode"] = False
            
        response = requests.post(
            f"{DEEPSEEK_API}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json=payload
        )
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({
            "error": "Proxy error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
