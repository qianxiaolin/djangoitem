from rest_framework import serializers
from market import models


# class GoodsInfoSerializer(serializers.ModelSerializer):
#     """商品信息序列化器"""
#
#     class Meta:
#         model = models.GoodsInfo
#         fields = '__all__'
#
#     def validate(self, attrs):
#         print('校验数据', attrs)
#         return attrs


class GoodsImgSerializer(serializers.ModelSerializer):
    """返回主键"""

    # 商品图片序列化器
    class Meta:
        model = models.GoodsImg
        fields = '__all__'


class GoodsShowSerializer(serializers.ModelSerializer):
    goods = GoodsImgSerializer(many=True, read_only=True)

    class Meta:
        model = models.GoodsInfo
        fields = ['goods_name', 'goods_concern', 'goods_description', 'id', 'goods']


    # 重写create，在商品信息模型和商品图片模型分别添加商品图片和商品信息
    def create(self, validated_data):
        print(validated_data)
        imgs = validated_data.pop('goods')
        goods= models.GoodsInfo.objects.create(**validated_data)
        for img in imgs:
            models.GoodsImg.objects.create(goods_id=goods, **img)
        return goods

    def validate(self, attrs):
        print('校验数据', attrs)
        return attrs