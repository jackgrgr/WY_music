from django.shortcuts import render, HttpResponse
from .models import SongList
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def get_avatar(request, param1):
    image_data = open("/home/boss/PycharmProjects/my_website/avatars/%s" % param1, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def index(request):
    lists_to_show = SongList.objects.order_by('list_play')[::-1][0:6]
    username = request.session.get('username', 'anonymous')
    password = request.session.get('password', '')
    user = authenticate(username=username, password=password)
    print(user)
    if user:
        login(request, user)
    return render(request, 'get_songlists/index.html', context={'lists_to_show': lists_to_show})


def order_by_list_fav(request):
    lists_to_show = SongList.objects.order_by('list_fav')[::-1][0:6]
    return render(request, 'get_songlists/favorite.html', context={'lists_to_show': lists_to_show})


def order_by_list_share(request):
    lists_to_show = SongList.objects.order_by('list_share')[::-1][0:6]
    return render(request, 'get_songlists/share.html', context={'lists_to_show': lists_to_show})


def order_by_list_comment(request):
    lists_to_show = SongList.objects.order_by('list_comment')[::-1][0:6]
    return render(request, 'get_songlists/comment.html', context={'lists_to_show': lists_to_show})
