import json
import urllib.parse
from bs4 import BeautifulSoup
import requests
from pytube import Playlist
import youtube_dl
import os
from . import settings
import time
from datetime import timedelta


def get_playlist_info(URL):
    playlistInfo = dict()
    playlist = Playlist(URL)
    playlist.populate_video_urls()
    urls = playlist.video_urls
    playlistInfo = get_video_details(urls[0])
    playlistInfo['title'] = playlist.title
    playlistInfo.update({
        'linkCount': len(playlist.video_urls)
    })
    return playlistInfo


def get_video_details(URL):
    info = extract_video_info(URL)
    video_data = dict()
    video_data.update({
        'uploader': f"{info['uploader']}",
        'title': f"{info['title']}",
        'thumbnail': info['thumbnail'],
        'description': f"{info['description']}"
    })
    return video_data


def get_video_formats(URL):
    info = extract_video_info(URL)
    videoData = dict()
    videoData.update({
        'uploader': f"{info['uploader']}",
        'title': f"{info['title']}",
        'thumbnail': info['thumbnail'],
        'description': f"{info['description']}"
    })
    formats = info['formats']
    videoData.update({
        'formats': {
            'video': [],
            'videoWoAudio': [],
            'audio': [],
            'others': []
        }
    })

    for format in formats:
        list = format['format'].split(' - ')
        if format['height'] != None and format['width'] != None:
            if format['asr'] == None and format['fps'] != None:
                videoData['formats']['videoWoAudio'].append({
                    'ext': f"{format['ext']}",
                    'format': f"{list[1]}",
                    'url': f"{format['url']}",
                    'asr': f"{format['asr']}",
                    'fps': f"{format['fps']}"
                })
            else:
                videoData['formats']['video'].append({
                    'ext': f"{format['ext']}",
                    'format': f"{list[1]}",
                    'url': f"{format['url']}",
                    'asr': f"{format['asr']}",
                    'fps': f"{format['fps']}"
                })
        elif format['height'] == None and format['width'] == None:
            videoData['formats']['audio'].append({
                'ext': f"{format['ext']}",
                'format': f"{list[1]}",
                'url': f"{format['url']}",
                'asr': f"{format['asr']}",
                'fps': f"{format['fps']}",
                'abr': f"{format['abr']}"
            })
        else:
            videoData['formats']['others'].append({
                'ext': f"{format['ext']}",
                'format': f"{list[1]}",
                'url': f"{format['url']}",
                'asr': f"{format['asr']}",
                'fps': f"{format['fps']}"
            })
    return videoData


def extract_video_info(URL):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            URL,
            download=False  # We just want to extract the info
        )
    return result


class YoutubeSearch:

    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self.search()

    def search(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        BASE_URL = "https://youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}&pbj=1"
        response = BeautifulSoup(requests.get(url).text, "html.parser")
        results = self.parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[:self.max_results]
        return results

    def parse_html(self, soup):
        results = []
        for video in soup.select(".yt-uix-tile-link"):
            if video["href"].startswith("/watch?v="):
                id = video["href"][video["href"].index("=") + 1:]
                video_info = {
                    "title": video["title"],
                    "link": "https://youtube.com" + video["href"],
                    "id": id,
                    'thumbnail': f"http://img.youtube.com/vi/{id}/0.jpg"
                }
                results.append(video_info)
        return results

    def to_dict(self):
        return self.videos

    def to_json(self):
        return json.dumps({"videos": self.videos}, indent=4)


def get_audio_info(URL):

    if not os.path.isdir(os.path.join(settings.BASE_DIR, 'static/media')):
        os.mkdir(
            os.path.join(settings.BASE_DIR, 'static/media')
        )
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(os.path.join(settings.BASE_DIR, 'static/media'), '%(id)s.%(ext)s'),
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        delete_expire_files()
        res = ydl.extract_info(URL, download=True)
        data = dict()
        data.update({
            'uploader': res['uploader'],
            'title': res['title'],
            'thumbnail': res['thumbnail'],
            'description': res['description'],
            'link': 'http://127.0.0.1:8000/static/media/'+f"{res['id']}.mp3",
        })

    return data


def delete_expire_files():
    files = os.listdir(os.path.join(settings.BASE_DIR, 'static/media'))
    for file in files:
        file_mod_time = os.stat(
            os.path.join(
                os.path.join(settings.BASE_DIR, 'static/media'), file
            )
        ).st_ctime
        expire_time = time.time()-5*60
        if file_mod_time < expire_time:
            os.remove(
                os.path.join(
                    os.path.join(settings.BASE_DIR, 'static/media'), file
                )
            )
