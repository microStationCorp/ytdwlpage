from django.http import HttpResponse
from django.shortcuts import render
# import pafy
import youtube_dl


def home(request):
    return render(request, 'index.html')


# def crawl(request):
#     url = request.GET.get('urlBox')
#     video = pafy.new(url)
#     strm = video.streams
#     html = []
#     for s in strm:
#         html.append({
#             'res': f"{s.resolution}",
#             'link': f"{s.url}"
#         })
#     return render(request, 'crawling.html', {'url': html})

def crawl(request):
    URL = request.GET.get('urlBox')
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            URL,
            download=False  # We just want to extract the info
        )
    formats = result['formats']
    html = []

    for item in formats:
        html.append({
            'format': f"{item['format']}",
            'url': f"{item['url']}"
        })
    return render(request, 'crawling.html', {'url': html})