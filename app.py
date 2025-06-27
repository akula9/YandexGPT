from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_input = data["request"]["original_utterance"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}],
        max_tokens=100
    )
    reply = response.choices[0].message.content

    return jsonify({
        "version": data["version"],
        "session": data["session"],
        "response": {
            "text": reply,
            "end_session": False
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
