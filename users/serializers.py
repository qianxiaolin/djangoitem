from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users import models
from rest_framework import exceptions


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义登录认证，使用自有用户表
    """
    username_field = 'username'

    def validate(self, attrs):
        authenticate_kwargs = {self.username_field: attrs[self.username_field], 'password': attrs['password']}
        print(authenticate_kwargs)
        try:
            user = models.User.objects.get(**authenticate_kwargs)
        except Exception as e:
            raise exceptions.NotFound(e.args[0])
        refresh = self.get_token(user)
        data = {"userId": user.id, "username": user.username, "token": str(refresh.access_token),
                "refresh": str(refresh), }
        return data


class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    class Meta:
        model = models.User()

    def create(self, validated_data):
        user = models.User.objects.create(**validated_data)
        return user

    def validate_account(self, value):
        print(value)
        try:
            user = models.User.objects.get(username=value).first()
            raise serializers.ValidationError({'message': '账号已存在'})
        except:
            return value

    def validate(self, attrs):
        print(attrs.get('password'))
        passwd = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if not passwd:
            raise serializers.ValidationError({'message': '密码不能为空'})
            return attrs
        elif not password_confirm:
            raise serializers.ValidationError({'message': '重复密码不能为空'})
        else:
            return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
        if instance.net_name:
            instance.net_name = validated_data.get('net_name')
        return instance

    def validate_avatar(self, avatar):
        print(avatar)
        if not avatar:
            raise serializers.ValidationError({'error': '上传失败，文件不能为空'})
        size = avatar.size
        if size > 1024 * 300:
            raise serializers.ValidationError({'error': "上传失败，文件大小不能超过300kb"})
        return avatar




