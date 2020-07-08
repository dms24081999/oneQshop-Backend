from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
from .authentication import *

# pyjwt decode --no-verify <TOKEN>
# import jwt
# jwt.decode('<TOKEN>', verify=False)

# jwt.encode(<PAYLOAD>, '<SECRET_KEY>', algorithm=['HS256']) => <TOKEN>
# jwt.decode('<TOKEN>','<SECRET_KEY>',algorithms=['HS256']) => <PAYLOAD>

# import time
# int(time.time())

from rest_framework import routers

router = routers.DefaultRouter()

# For listing all users and creating new user, to view a single user append '/1' that is '/id' in the URL  path 'list/fullinfo'
router.register(r"list/fullinfo", FullInfoListViewUsersAPIView)

urlpatterns = [
    path('login/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/token/custom/', MyTokenObtainPairView.as_view()),
    path("", include(router.urls)),
    # path("user/currentuser/", CurrentUserAPIView.as_view()),
]

