import os
from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)

# 🔑 Required for chat history (sessions)
app.secret_key = "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"

# 🔑 API key from Render Environment Variables
API_KEY = os.getenv("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")

@app.route("/", methods=["GET", "POST"])
def home():

    if "chat" not in session:
        session["chat"] = []

    if request.method == "POST":
        user_msg = request.form.get("message")

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": user_msg}
            ]
        }

        try:
            res = requests.post(url, headers=headers, json=data)
            result = res.json()

            print(result)  # debug on Render logs

            if "choices" in result:
                reply = result["choices"][0]["message"]["content"]
            else:
                reply = "API Error: " + str(result)

        except Exception as e:
            reply = f"Error: {str(e)}"

        # 💾 Save chat history
        chat = session["chat"]
        chat.append({"user": user_msg, "ai": reply})
        session["chat"] = chat

    return render_template("index.html", chat=session["chat"])

# 🌍 Render production run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
