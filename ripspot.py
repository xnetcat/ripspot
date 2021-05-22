import sys
import argparse
import os
import pathlib
import subprocess
import shutil


from librespot.audio.decoders import AudioQuality
from librespot.core import Session
from librespot.metadata import TrackId
from librespot.player.codecs import VorbisOnlyAudioQuality

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from utils import _download_song

try:
    subprocess.Popen(
        ["ffmpeg", "-version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
except FileNotFoundError:
    print("install ffmpeg", file=sys.stderr)
    sys.exit(1)

parser = argparse.ArgumentParser(
    description="Simple spotify ripper, that converts downloaded songs to mp3 and tags them with spotify metadata",
    prog="ripspot",
)
parser.add_argument("url", type=str, nargs="+", help="URL to a song/album/playlist")
parser.add_argument("-u", "--username", help="Your spotify username", required=True)
parser.add_argument("-p", "--password", help="Your spotify password", required=True)
parser.add_argument(
    "-q",
    "--quality",
    help="Select your prefered quality",
    choices={"normal", "high", "veryhigh"},
    default="normal",
)

arguments = parser.parse_args()

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id="efda7d91569a4df89c9862a54b04d6c5",
        client_secret="e53ec07ea6224e48a8b32813cb55c08c",
    )
)

session = (
    Session.Builder()
    .user_pass(username=arguments.username, password=arguments.password)
    .create()
)

temp_folder = pathlib.Path(".", "riptemp")

if not temp_folder.exists():
    temp_folder.mkdir()

tracks = []
for request in arguments.url:
    if "open.spotify.com" in request and "track" in request:
        tracks.append(spotify.track(request))
    elif "open.spotify.com" in request and "playlist" in request:
        playlist = spotify.playlist(request)

        while playlist:
            playlist_tracks = playlist.get("tracks")

            if playlist_tracks is not None:
                playlist_tracks = playlist_tracks.get("items")

                if len(playlist_tracks) > 0:
                    tracks.extend(
                        [
                            track["track"]
                            for track in playlist_tracks
                            if "track" in track
                        ]
                    )

                if playlist["tracks"]["next"]:
                    playlist = spotify.next(playlist["tracks"])
                else:
                    playlist = None
            else:
                playlist = None
    elif "open.spotify.com" in request and "album" in request:
        album = spotify.album(request)

        while album:
            album_tracks = album.get("tracks")

            if album_tracks is not None:
                album_tracks = album_tracks.get("items")

                if len(album_tracks) > 0:
                    for track in album_tracks:
                        track.update(
                            {
                                "album": {
                                    "images": album["images"],
                                    "release_date": album["release_date"],
                                    "name": album["name"],
                                }
                            }
                        )

                    tracks.extend(album_tracks)

                if album["tracks"]["next"]:
                    album = spotify.next(album["tracks"])
                else:
                    album = None
            else:
                album = None

for track in tracks:
    _download_song(session, track, arguments.quality)

shutil.rmtree(temp_folder)
