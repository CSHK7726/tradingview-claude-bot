from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    alert_message = data.get("message", "No message received")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"TradingView alert: '{alert_message}'. Give me a brief trading analysis and recommendation."
            }
        ]
    )

    claude_response = response.content[0].text
    print(f"Alert: {alert_message}")
    print(f"Claude says: {claude_response}")
    return jsonify({"status": "ok", "analysis": claude_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
