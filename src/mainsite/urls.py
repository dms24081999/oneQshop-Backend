"""mainsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin

admin.site.site_header = "one-Q-shop Admin"
admin.site.site_title = "one-Q-shop Admin Portal"
admin.site.index_title = "Welcome to one-Q-shop Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/login/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/login/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/users/", include("users_app.urls")),
    path("api/products/", include("products_app.urls")),
]

if not settings.AWS:
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


"""
pyjwt decode --no-verify <TOKEN>
import jwt
jwt.decode('<TOKEN>', verify=False)

jwt.encode(<PAYLOAD>, '<SECRET_KEY>', algorithm=['HS256']) => <TOKEN>
jwt.decode('<TOKEN>','<SECRET_KEY>',algorithms=['HS256']) => <PAYLOAD>

import time
int(time.time())
"""
