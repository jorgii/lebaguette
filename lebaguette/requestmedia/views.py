from django.shortcuts import render


def request_media(request):
    return render(request, 'requestmedia/request_media.html')
