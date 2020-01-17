from django.http import HttpResponse
from django.shortcuts import render
# import pafy
import youtube_dl


def home(request):
    URL = request.GET.get('urlBox')
    if URL != None:
        try:
            ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

            with ydl:
                result = ydl.extract_info(
                    URL,
                    download=False  # We just want to extract the info
                )
            if 'entries' in result:
                return render(request, 'index.html', {'mflag': 'True'})
            html = dict()
            html.update({
                'uploader': f"{result['uploader']}",
                'title': f"{result['title']}",
                'thumbnail': result['thumbnail'],
                'description': f"{result['description']}"
            })
            formats = result['formats']
            html.update({
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
                        html['formats']['videoWoAudio'].append({
                            'ext': f"{format['ext']}",
                            'format': f"{list[1]}",
                            'url': f"{format['url']}",
                            'asr': f"{format['asr']}",
                            'fps': f"{format['fps']}"
                        })
                    else:
                        html['formats']['video'].append({
                            'ext': f"{format['ext']}",
                            'format': f"{list[1]}",
                            'url': f"{format['url']}",
                            'asr': f"{format['asr']}",
                            'fps': f"{format['fps']}"
                        })
                elif format['height'] == None and format['width'] == None:
                    html['formats']['audio'].append({
                        'ext': f"{format['ext']}",
                        'format': f"{list[1]}",
                        'url': f"{format['url']}",
                        'asr': f"{format['asr']}",
                        'fps': f"{format['fps']}",
                        'abr': f"{format['abr']}"
                    })
                else:
                    html['formats']['others'].append({
                        'ext': f"{format['ext']}",
                        'format': f"{list[1]}",
                        'url': f"{format['url']}",
                        'asr': f"{format['asr']}",
                        'fps': f"{format['fps']}"
                    })
            return render(request, 'index.html', {'aflag': 'True', 'dataDict': html})
        except:
            return render(request, 'index.html', {'eflag': 'True'})
    else:
        return render(request, 'index.html')
