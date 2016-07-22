from django.db import models


# Create your models here.
class SongList(models.Model):
    list_name = models.CharField(max_length=100)
    list_link = models.CharField(max_length=100, default='')
    list_id = models.IntegerField(primary_key=True, default=0)
    list_img = models.CharField(max_length=200, default='')
    list_author = models.CharField(max_length=100, default='GR')
    list_created_date = models.DateField(default='1991-02-26')
    list_play = models.IntegerField(default=0)
    list_fav = models.IntegerField(default=0)
    list_share = models.IntegerField(default=0)
    list_comment = models.IntegerField(default=0)

    def __str__(self):
        return self.list_name
