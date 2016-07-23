from django.shortcuts import render, HttpResponse
from .models import SongList
import numpy as np


# Create your views here.
def get_avatar(request, param1):
    image_data = open("/home/boss/PycharmProjects/my_website/avatars/%s" % param1, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def index(request):
    lists_to_show = SongList.objects.order_by('list_play')[::-1][0:6]
    all_lists = SongList.objects.all()
    average_play = 0
    list_numplay = [list_.list_play / 10000 for list_ in all_lists]
    average_play += int(np.mean(list_numplay) * 10000)
    var_play = np.sqrt(np.var(list_numplay)) * (10 ** 4)
    print(average_play, var_play)

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
