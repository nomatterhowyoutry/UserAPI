from .views import (PostRudView,
                    PostAPIView,
                    LikeAPIView,
                    DislikeAPIView)
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', PostRudView.as_view(), name='postRud'),
    url(r'^$', PostAPIView.as_view(), name='post-create'),
    url(r'^like/(?P<pk>\d+)/$', LikeAPIView.as_view(), name='like'),
    url(r'^dislike/(?P<pk>\d+)/$', DislikeAPIView.as_view(), name='dislike'),
]
