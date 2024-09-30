from constants import CLIENT_ID, CLIENT_SECRET, API_BASE_URL, TOKEN_URL
from datetime import datetime
from flask import redirect, session
from functools import wraps

import requests

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if session.get("refresh_token") == None or session.get("access_token") == None:
            return redirect('/login')
        
        if datetime.now().timestamp() > session["expires_at"]:
            req_body = {
            "grant_type" : "refresh_token",
            "refresh_token" : session["refresh_token"],
            "client_id" : CLIENT_ID,
            "client_secret" : CLIENT_SECRET
            }

            response = requests.post(TOKEN_URL, data = req_body)
            new_token_info = response.json()

            session["access_token"] = new_token_info["access_token"]
            session["expires_at"] = datetime.now().timestamp() + new_token_info["expires_in"]

        func(*args, **kwargs)
    return wrapper

@token_required
def get_user_info():
    headers = {
        "Authorization" : f"Bearer {session["access_token"]}"
    }

    response = requests.get(API_BASE_URL + 'me', headers=headers)
    user_info = response.json()

    return user_info

@token_required
def get_playlists():
    
    headers = {
        "Authorization" : f"Bearer {session["access_token"]}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()

    return playlists

@token_required
def get_top_items(items_type:str):

    headers = {
        "Authorization" : f"Bearer {session["access_token"]}"
    }

    response = requests.get(API_BASE_URL + "me/top/" + items_type, headers=headers)
    items = response.json()
        
    return items

@token_required
def get_recently_played():
    
    headers = {
        "Authorization" : f"Bearer {session["access_token"]}"
    }

    response = requests.get(API_BASE_URL + "me/player/recently-played", headers=headers)
    items = response.json()
        
    return items

@token_required
def get_tracks(tracks : list[str]):

    headers = {
        "Authorization" : f"Bearer {session["access_token"]}"
    }

    if len(tracks) == 0:
        return 
    if len(tracks) == 1:
        url = API_BASE_URL + "tracks/" + tracks[0]
        response = requests.get(url, headers=headers)
        items = response.json()
    else:
        params = {
            "ids" : tracks.join(",")
        }
        url = API_BASE_URL + "tracks"
        response = requests.get(url, headers=headers, params=params)
        items = response.json()

    return items
         



    