import json
import os
import time

import requests

USER_ID = "1219121420"
PAGE_SIZE = 50


def get_token():
    r = requests.post(
        url="https://accounts.spotify.com/api/token",
        headers={"Content-type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": os.environ["SPOTIFY_CLIENT_ID"],
            "client_secret": os.environ["SPOTIFY_CLIENT_SECRET"],
        },
    )
    r.raise_for_status()
    return r.json()["access_token"]


def _get_playlists_page(page_num=1):

    offset = page_num * PAGE_SIZE

    token = get_token()
    r = requests.get(
        url=f"https://api.spotify.com/v1/users/{USER_ID}/playlists",
        headers={"Authorization": f"Bearer {token}"},
        params={"limit": PAGE_SIZE, "offset": offset},
    )
    r.raise_for_status()
    return r.json()


def get_playlists():
    page = 0
    all_playlists = []

    while True:
        response = _get_playlists_page(page)
        batch_playlists = response['items']
        all_playlists += batch_playlists
        if len(batch_playlists) < 50:
            break
        page += 1
        time.sleep(3)

    return all_playlists


if __name__ == "__main__":
    playlists = get_playlists()
    for playlist in playlists:
        print(json.dumps(playlist))
