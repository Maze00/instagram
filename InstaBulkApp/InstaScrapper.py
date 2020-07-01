import sys
import requests
import time
import urllib.request
import os
import json
from django.conf import settings as conf_settings

Sources = []

def getSource(index_):
    return Sources[index_]

def validateProfile(instagram_username):
    page = requests.get('https://www.instagram.com/' + instagram_username + '/?__a=1')
    
    if page.status_code != 200: 
        return False
    
    page = page.json()
    
    if page['graphql']['user']['is_private']:
        return False
    
    return True

def get_user_id(html):
    return html.json()["graphql"]["user"]["id"]

def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def Scrap_it(instagram_username, nextpagcode):
    Sources = []
    html = requests.get("https://www.instagram.com/" + instagram_username + "/?__a=1")
    
    user_id = int(get_user_id(html))
    
    url = conf_settings.URL_PATH
    data = {"username": instagram_username, "userid": user_id, "page": nextpagcode}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, json=data, headers=headers)
    for match in r.json()["media"]:        
        Sources.append(match["download_src"])
        
    return Sources,r.json()["next_page"]
