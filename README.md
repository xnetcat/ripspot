# ripspot
Spotify ripper

# Prerequisites

- Python

# Libs

- librespot-python - `pip install git+https://github.com/kokarare1212/librespot-python`
- spotipy - `pip install spotipy`
- mutagen - `pip install mutagen`

# How to run

`python ripspot.py --username "username" --password "password" [links]`

example:

to download album
- `python ripspot.py --username "username" --password "password" https://open.spotify.com/album/39gNIUdLlihrdSDu1BpzEX`

to download song
- `python ripspot.py --username "username" --password "password" https://open.spotify.com/track/62VJE7RsgsmjjmI2eHH4lx`

to download song album and playlist
- `python ripspot.py --username "username" --password "password" https://open.spotify.com/track/62VJE7RsgsmjjmI2eHH4lx https://open.spotify.com/playlist/5tFLvXM5ieVn8wzCaLTuzt https://open.spotify.com/album/2SYoVgjmUEYmzwP42lROTx`
