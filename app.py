import os
from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)
    return response

@app.route("/receive_signal", methods=["POST"])
def receive_signal():
    data = request.get_json()
    if data and "message" in data:
        signal = data["message"]

        # تحديد نوع الصفقة
        direction = "شراء" if "BUY" in signal.upper() else "بيع" if "SELL" in signal.upper() else "غير معروف"

        reply = f"📈 توصية {direction}:\n{signal}"
        send_to_telegram(reply)
        return "OK", 200
    return "Bad Request", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)