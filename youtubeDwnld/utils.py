import json
from isodate import parse_duration
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


class YoutubeSearch:
    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
    VIDEO_URL = 'https://www.googleapis.com/youtube/v3/videos'
    BASE_URL = 'https://www.youtube.com/watch?v='

    def __init__(self, search_term):
        self.search_term = search_term
        self.ids = self.get_video_id(self.search_term)
        self.video_data = self.get_videos(self.ids)

    def get_video_id(self, query):
        search_params = {
            'part': 'snippet',
            'q': query,
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 20,
            'type': 'video',
            'order': 'relevance'
        }
        sRe = requests.get(self.SEARCH_URL, params=search_params)
        search_res = sRe.json()['items']
        video_id = []
        for item in search_res:
            video_id.append(item['id']['videoId'])
        return video_id

    def get_videos(self, id):
        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(id)
        }

        vRe = requests.get(self.VIDEO_URL, params=video_params)

        video_res = vRe.json()['items']
        videos = []
        for item in video_res:
            videos.append({
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'url': f"{self.BASE_URL}{item['id']}",
                'channel': item['snippet']['channelTitle'],
                'duration': f"{parse_duration(item['contentDetails']['duration'])}"
            })
        return videos
