from django.db import models
from users.models import User


class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=24)
    goods_price = models.IntegerField(null=True)
    goods_concern = models.IntegerField(default=0,null=False)
    goods_description = models.TextField(null=True)
    goods_publish_time = models.TimeField(auto_now_add=True)


class GoodsImg(models.Model):
    goods_img = models.ImageField(null=True)
    goods_id = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="所属商品")









