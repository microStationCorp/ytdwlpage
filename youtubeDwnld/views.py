from django.http import HttpResponse
from django.shortcuts import render
import youtube_dl
from . import utils


def home(request):
    URL = request.GET.get('urlBox')
    if URL == None:
        return render(request, 'index.html')
    elif URL == '':
        return render(request, 'index.html', {'nflag': 'True'})
    else:
        try:
            if URL.find('list') != -1:
                playlist_info = utils.get_playlist_info(URL)
                return render(request, 'index.html', {'mflag': 'True', 'dataDict': playlist_info})
            else:
                video_data = utils.get_video_formats(URL)
                return render(request, 'index.html', {'aflag': 'True', 'dataDict': video_data})
        except:
            return render(request, 'index.html', {'eflag': 'True'})


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
        resultDict = utils.YoutubeSearch(query).video_data
        if len(resultDict) != 0:
            return render(request, 'search.html', {'sflag': 'True', 'resultDict': resultDict})
        else:
            return render(request, 'search.html', {'eflag': 'True', 'query': query})


def audio(request):
    URL = request.GET.get('audioURL')
    if URL == None:
        return render(request, 'audio.html')
    elif URL == '':
        return render(request, 'audio.html', {'nflag': 'True'})
    else:
        try:
            if URL.find('list') != -1:
                playlist_info = utils.get_playlist_info(URL)
                return render(request, 'index.html', {'mflag': 'True', 'dataDict': playlist_info})
            else:
                audioData = utils.get_audio_info(URL)
                return render(request, 'audio.html', {'auflag': 'True', 'audioData': audioData})
        except:
            return render(request, 'audio.html', {'eflag': 'true'})
