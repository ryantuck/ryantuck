import json
import sys


def playlist_track(input_obj):
    return {
        'title': input_obj['track']['name'],
        'artists': [artist['name'] for artist in input_obj['track']['artists']],
    }

if __name__ == '__main__':
    arg = sys.argv[1]

    if arg == 'playlist-track':
        for line in sys.stdin:
            input_obj = json.loads(line)
            print(json.dumps(playlist_track(input_obj)))