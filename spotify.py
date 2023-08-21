import json
import os
import sys
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



def _get(url, page_num=0):
    offset = page_num * PAGE_SIZE
    token = get_token()
    r = requests.get(
        url=url,
        headers={"Authorization": f"Bearer {token}"},
        params={"limit": PAGE_SIZE, "offset": offset},
    )
    r.raise_for_status()
    return r.json()


def _get_playlists(page_num=0):
    return _get(
        url=f"https://api.spotify.com/v1/users/{USER_ID}/playlists",
        page_num=page_num,
    )['items']


def _get_playlist_tracks(playlist_id, page_num=0):
    return _get(
        url=f"https://api.spotify.com/v1/users/{USER_ID}/playlists/{playlist_id}/tracks",
        page_num=page_num,
    )['items']


def get_playlists():
    page = 0
    all_results = []

    while True:
        batch = _get_playlists(page_num=page)
        all_results += batch
        if len(batch) < PAGE_SIZE:
            break
        page += 1
        time.sleep(3)

    return all_results


def get_playlist_tracks(playlist_id):
    page = 0
    all_results = []

    while True:
        batch = _get_playlist_tracks(playlist_id, page_num=page)
        all_results += batch
        if len(batch) < PAGE_SIZE:
            break
        page += 1
        time.sleep(3)

    return all_results


if __name__ == "__main__":
    arg = sys.argv[1]

    if arg == 'playlists':
        playlists = get_playlists()
        for playlist in playlists:
            print(json.dumps(playlist))

    if arg == 'playlist-tracks':
        playlist_id = sys.argv[2]
        tracks = get_playlist_tracks(playlist_id)
        for track in tracks:
            print(json.dumps(track))