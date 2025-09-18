from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = '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'
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    payload = {
        "model": "gpt-3.5-turbo", 
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "max_tokens": 150
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        bot_reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": bot_reply})
    else:
        return jsonify({"error": "API request failed", "details": response.text}), 500

if __name__ == "__main__":
    app.run(debug=True)