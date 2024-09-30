from constants import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, SCOPE
from datetime import datetime
from flask import Flask, redirect, render_template, jsonify, request, session
from helpers import *

import requests
import urllib.parse

app = Flask(__name__)
app.secret_key = "kjdvblkdblvwppqnkcb"

@token_required
@app.route("/")
def index():
    session["user_info"] = get_user_info()
    return render_template("index.html")

@app.route("/login")
def login():

    params = {
        "client_id" : CLIENT_ID,
        "response_type" : "code",
        "scope" : SCOPE,
        "redirect_uri" : REDIRECT_URI,
        "show_dialog" : True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route("/callback")
def callback():
    if "error" in request.args:
        return jsonify({"error" : request.args["error"]})
    
    if "code" in request.args:
        req_body = {
            "code" : request.args['code'],
            "grant_type" : "authorization_code",
            "redirect_uri" : REDIRECT_URI,
            "client_id" : CLIENT_ID,
            "client_secret" : CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session["access_token"] = token_info["access_token"]
        session["refresh_token"] = token_info["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]

        return redirect("/")

@token_required  
@app.route("/logout")
def logout():
    session.clear()
    return "bye!"

@app.route("/top-items")
def top_items():
    items = get_top_items("tracks")
    print(items)
    return items 

@app.route("/recently-played")
def recently_played():
    items = get_recently_played()
    return items