from django.urls import path, include
from mywell.views import *

from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions

app_name = 'mywell'


router = routers.DefaultRouter()
router.register('Account',AccountView)
router.register('project',projectView)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),
    path('addgroup/', CustomGroupView.as_view()),
    path('project/', projectAPI.as_view()),
    path('project_detail/', projectdetailAPI.as_view()),
    path('auth_login/', CustomAuthToken.as_view()),

]