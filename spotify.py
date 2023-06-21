import json
import os

import requests

USER_ID = "1219121420"


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


def get_playlists():
    # TODO paginate
    token = get_token()
    r = requests.get(
        url=f"https://api.spotify.com/v1/users/{USER_ID}/playlists",
        headers={"Authorization": f"Bearer {token}"},
        params={"limit": 50},
    )
    r.raise_for_status()
    return r.json()["items"]


if __name__ == "__main__":
    playlists = get_playlists()
    for playlist in playlists:
        print(json.dumps(playlist))
