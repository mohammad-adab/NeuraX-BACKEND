from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# SMTP Email Configuration (Replace with your own)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

def send_email(name, email):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Welcome to NeuraX!"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg.set_content(f"Hello {name},\n\nWelcome to NeuraX! Your registration is confirmed.\n\nBest Regards,\nThe NeuraX Team")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if send_email(name, email):
        return jsonify({"message": "✅ Registration successful! Confirmation email sent."})
    else:
        return jsonify({"message": "❌ Registration failed. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True)
