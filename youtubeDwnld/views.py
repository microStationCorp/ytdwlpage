from django.http import HttpResponse
from django.shortcuts import render
import youtube_dl
from . import utils


def home(request):
    URL = request.GET.get('urlBox')
    if URL != None:
        try:
            if URL.find('list') != -1:
                playlist_info = utils.get_playlist_info(URL)
                return render(request, 'index.html', {'mflag': 'True', 'dataDict': playlist_info})
            else:
                video_data = utils.get_video_formats(URL)
                return render(request, 'index.html', {'aflag': 'True', 'dataDict': video_data})
        except:
            return render(request, 'index.html', {'eflag': 'True'})
    else:
        return render(request, 'index.html')


def dmca(request):
    return render(request, 'DMCA.html')


def cu(request):
    return render(request, 'cu.html')


def docp(request):
    return render(request, 'docpage.html')


def search(request):
    query = request.GET.get('searchName')
    if query == None:
        return render(request, 'search.html')
    else:
        video_info = utils.YoutubeSearch(query, max_results=10).to_dict()
        resultDict = []
        if len(video_info) != 0:
            for item in video_info:
                resultDict.append({
                    'title': item['title'],
                    'link': item['link'],
                    'thumbnail': item['thumbnail']
                })
            return render(request, 'search.html', {'sflag': 'True', 'resultDict': resultDict})
        else:
            return render(request, 'search.html', {'eflag': 'True'})


def audio(request):
    URL = request.GET.get('audioURL')
    if URL != None:
        try:
            if URL.find('list') != -1:
                playlist_info = utils.get_playlist_info(URL)
                return render(request, 'index.html', {'mflag': 'True', 'dataDict': playlist_info})
            else:
                audioData = utils.get_audio_info(URL)
                return render(request, 'audio.html', {'auflag': 'True', 'audioData': audioData})
        except:
            return render(request, 'audio.html', {'eflag': 'true'})
    else:
        return render(request, 'audio.html', {'nflag': 'True'})
