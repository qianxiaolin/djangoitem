
from users import views

from django.urls import path, re_path, include


from django.conf import settings

from django.conf.urls.static import static
urlpatterns = [
    path('api/login/verify', views.LoginView.as_view()),
    path('api/login/register', views.RegisterView.as_view({'post': 'create'})),
    path('api/user/info/update', views.UserView.as_view({'post': 'update_user'})),
    path('api/user/info/get', views.UserView.as_view({'get': 'list_userinfo'})),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
