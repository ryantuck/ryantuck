playlists.md : playlists.jsonl
	echo "# Spotify Playlists" > $@
	cat $< | jq -r '"-  [\(.name)](\(.url))"' >> $@

playlists.jsonl : 
	python spotify.py | jq -c '{"name": .name, "url": .external_urls.spotify}' > $@