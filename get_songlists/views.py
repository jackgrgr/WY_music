from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import SongList
from django import forms
import numpy as np


# Create your views here.
def get_avatar(request, param1):
    image_data = open("/home/boss/PycharmProjects/my_website/avatars/%s" % param1, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def index(request):
    lists_order_by_play = SongList.objects.order_by('list_play')[::-1]
    return render(request, 'get_songlists/index.html', context={'lists_to_show': lists_order_by_play[0:6]})


def order_by_list_fav(request):
    lists_to_show = SongList.objects.order_by('list_fav')[::-1][0:6]
    return render(request, 'get_songlists/favorite.html', context={'lists_to_show': lists_to_show})


def order_by_list_share(request):
    lists_to_show = SongList.objects.order_by('list_share')[::-1][0:6]
    return render(request, 'get_songlists/share.html', context={'lists_to_show': lists_to_show})


def order_by_list_comment(request):
    lists_to_show = SongList.objects.order_by('list_comment')[::-1][0:6]
    return render(request, 'get_songlists/comment.html', context={'lists_to_show': lists_to_show})


class QueryForm(forms.Form):
    query_id = forms.CharField()


def spider_web(request):
    query_id = request.GET.get('query_id')
    lists_order_by_play = SongList.objects.order_by('list_play')
    numplay_list = [list_.list_play for list_ in lists_order_by_play]
    lists_order_by_fav = SongList.objects.order_by('list_fav')
    numfav_list = [list_.list_fav for list_ in lists_order_by_fav]
    lists_order_by_share = SongList.objects.order_by('list_share')
    numshare_list = [list_.list_share for list_ in lists_order_by_share]
    lists_order_by_comment = SongList.objects.order_by('list_comment')
    numcomment_list = [list_.list_comment for list_ in lists_order_by_comment]
    query_list = SongList.objects.get(list_id=query_id)
    num_lists = len(lists_order_by_play)
    index_dict = dict()
    index_dict['play_index'] = (numplay_list.index(query_list.list_play) + 1) / num_lists
    index_dict['fav_index'] = (numfav_list.index(query_list.list_fav) + 1) / num_lists
    index_dict['share_index'] = (numshare_list.index(query_list.list_share) + 1) / num_lists
    index_dict['comment_index'] = (numcomment_list.index(query_list.list_comment) + 1) / num_lists
    print(index_dict)
    return JsonResponse(index_dict)
    # list_numplay = [list_.list_play / 10000 for list_ in lists_order_by_play]
    # average_play = int(np.mean(list_numplay) * 10000)
    # var_play = int(np.sqrt(np.var(list_numplay)) * (10 ** 4))
