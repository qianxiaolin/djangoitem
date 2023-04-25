from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from common.permissions import MyPermission
from common.jwt import MyJWTAuthentication
from market import models
from market import serializers


class SecondMarketView(APIView):
    authentication_classes = [MyJWTAuthentication]
    permission_classes = [MyPermission]
    queryset = models.GoodsInfo.objects.all()
    serializer_class = serializers.GoodsShowSerializer

    def get(self, request, *args, **kwargs):
        """"查询商品数据集"""
        # 获取二手出售商品的信息
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        serializer.data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print(data)
        good = self.serializer_class(data=data)
        if good.is_valid():
            good.save()
            return Response({'code': 200, "message": 'SUCCESS'})
        else:
            print(good.errors)
            return Response({'code': 400, "message": 'ERROR'})


