from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework_simplejwt.views import TokenObtainPairView
from common.jwt import MyJWTAuthentication
from users import serializers
from users.serializers import MyTokenObtainPairSerializer, RegisterSerializer
from users import models
from common.permissions import MyPermission

# 用户登录
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LoginView(MyTokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({'message': '账号或密码不存在'}, status=status.HTTP_400_BAD_REQUEST)
        result = serializer.validated_data
        return Response(result, status=status.HTTP_200_OK)


# 注册
class RegisterView(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = models.User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        res = serializer.is_valid()
        if res:
            user = serializer.save()
            return Response({'status_code': '200', 'message': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'status_code': '400', 'message': '用户已存在'}, status=status.HTTP_400_BAD_REQUEST)

# 用户视图
class UserView(viewsets.ModelViewSet):
    authentication_classes = [MyJWTAuthentication]
    permission_classes = [MyPermission]
    queryset = models.User.objects.all
    serializer_class = serializers.UserSerializer

    # 上传头像
    def get_object(self):
        return self.request.user
    def get_sex(self,sex):
        dict1 = {'0': '女','1': '男','2': '秘密'}
        return dict1[str(sex)]
    # 得到用户信息
    def list_userinfo(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        sex = self.get_sex(serializer.data['sex'])
        return Response({'url': str(serializer.data['avatar']), 'birthday': str(serializer.data['birthday']),
                         'self_describe': str(serializer.data['self_describe']),'sex': sex,
                         'college': serializer.data['college'], 'major': serializer.data['major'],
                         'net_name': str(serializer.data['net_name'])
                         }, status=status.HTTP_200_OK)

    def update_user(self, request, *args, **kwargs):
        print('requestdata', request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            # print(serializer.errors)
            return Response({'message': '失败'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)

