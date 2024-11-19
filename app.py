from flask import Flask, redirect, request, session, url_for
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with a secure key in production

# GitHub OAuth configuration
CLIENT_ID = "your_client_id"  # Replace with your GitHub Client ID
CLIENT_SECRET = "your_client_secret"  # Replace with your GitHub Client Secret
AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"


@app.route("/")
def home():
    return "<a href='/login'>Log in with GitHub</a>"


@app.route("/login")
def login():
    # Redirect user to GitHub for authorization
    return redirect(f"{AUTHORIZE_URL}?client_id={CLIENT_ID}&scope=read:user")


@app.route("/callback")
def callback():
    # Exchange the code for an access token
    code = request.args.get("code")
    if not code:
        return "Error: No code provided", 400

    # Request access token
    token_response = requests.post(
        TOKEN_URL,
        headers={"Accept": "application/json"},
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
        },
    )
    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return "Error: Unable to fetch access token", 400

    # Optionally, get user data
    user_response = requests.get(
        USER_API_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_data = user_response.json()

    # Display access token and user information
    return f"""
    <h1>Welcome, {user_data.get('login')}!</h1>
    <p>Your access token is:</p>
    <code>{access_token}</code>
    """


if __name__ == "__main__":
    app.run(debug=True)
