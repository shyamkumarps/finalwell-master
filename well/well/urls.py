
from django.contrib import admin
from django.urls import path,include
from mywell.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', ObtainAuthTokenView.as_view(), name="login"),
    path('', include('mywell.urls')),
]
