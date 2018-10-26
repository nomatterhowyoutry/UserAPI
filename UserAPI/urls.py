from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^api/posts/', include('posts.api.urls')),
    url('^api/auth/', include('rest_auth.urls')),
    url('^api/auth/register/', include('rest_auth.registration.urls')),
    url('^login/', obtain_jwt_token),
]
