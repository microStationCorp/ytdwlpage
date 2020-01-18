from pytube import Playlist
import youtube_dl


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


def get_video_formats(URL, videoData):
    info = extract_video_info(URL)
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
