from flask import Flask, request

app = Flask(__name__)

@app.route("/callback")
def callback():
    """Captures the authorization code from the Spotify redirect URL."""
    auth_code = request.args.get("code")
    if auth_code:
        return f"Authorization Code: {auth_code}"
    else:
        return "Error: No authorization code found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)