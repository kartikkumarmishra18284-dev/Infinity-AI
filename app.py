import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 🔑 API key comes from Render Environment Variables
API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():

    reply = ""
    user_msg = ""

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

            print("DEBUG:", result)  # shows errors in Render logs

            if "choices" in result:
                reply = result["choices"][0]["message"]["content"]
            else:
                reply = "API Error: " + str(result)

        except Exception as e:
            reply = f"Error: {str(e)}"

    return render_template("index.html", user_msg=user_msg, reply=reply)


# 🌍 Render deployment setting
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
