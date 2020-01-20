from django.http import HttpResponse
from django.shortcuts import render
import youtube_dl
from . import utils
from youtube_search import YoutubeSearch


def home(request):
    URL = request.GET.get('urlBox')
    if URL != None:
        try:
            if URL.find('list') != -1:  # if true it is a playlist
                playlist_info = utils.get_playlist_info(URL)
                return render(request, 'index.html', {'mflag': 'True', 'dataDict': playlist_info})
            else:
                video_data = utils.get_video_details(
                    URL)  # get the video details
                video_data = utils.get_video_formats(
                    URL, video_data)  # get the video formats
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
        video_info = YoutubeSearch(query, max_results=10).to_dict()
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
