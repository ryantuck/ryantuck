playlists.md : playlists.jsonl
	echo "# Spotify Playlists" > $@
	cat $< | jq -r '"-  [\(.name)](\(.url))"' >> $@

playlists.jsonl : playlists-raw.jsonl
	cat $< | jq -c '{"name": .name, "url": .external_urls.spotify}' > $@

playlists-raw.jsonl :
	python spotify.py playlists | jq -c > $@

playlist-ids.txt : playlists-raw.jsonl
	cat $< | jq .id -r > $@

# TODO use patsubst etc
playlist-tracks.txt : playlist-ids.txt
	rm -f $@
	cat $< | xargs --verbose -I % sh -c 'python spotify.py playlist-tracks % | jq -c > playlist-tracks/%.jsonl && echo % >> $@'



# -------------------------------------
# Almost-ideal setup below for playlist tracks for indeterminate amount of playlists to pull for
# Don't have API fetch parallelization via make fully down, relying on xargs in the meantime

# PLAYLIST_IDS := $(shell cat playlist-ids.txt)
# TARGET_PLAYLISTS := $(patsubst %, playlist-tracks/%.jsonl, $(PLAYLIST_IDS))

# .PHONY : all-playlist-tracks
# all-playlist-tracks : $(TARGET_PLAYLISTS)

# playlist-tracks/%.jsonl :
# 	python spotify.py playlist-tracks $(basename $(notdir $@)) | jq -c > $@