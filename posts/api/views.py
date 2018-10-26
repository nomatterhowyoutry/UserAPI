from rest_framework import generics, mixins
from posts.models import Post, LikeDislike
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
import json


User = get_user_model()


class PostAPIView(mixins.CreateModelMixin, generics.ListAPIView):

    lookup_field        = 'pk'
    serializer_class    = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class PostRudView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field        = 'pk'
    serializer_class    = PostSerializer
    permission_classes  = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class LikeAPIView(generics.CreateAPIView):

    lookup_field        = 'pk'
    serializer_class    = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    model = Post
    vote_type = 1

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        if result:
            return HttpResponse(
                json.dumps({
                    "result": result,
                    "like_count": obj.votes.likes().count(),
                    "dislike_count": obj.votes.dislikes().count(),
                    "sum_rating": obj.votes.sum_rating()
                }),
                content_type="application/json"
            )


class DislikeAPIView(generics.CreateAPIView):

    lookup_field        = 'pk'
    serializer_class    = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    model = Post
    vote_type = -1

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        if result:
            return HttpResponse(
                json.dumps({
                    "result": result,
                    "like_count": obj.votes.likes().count(),
                    "dislike_count": obj.votes.dislikes().count(),
                    "sum_rating": obj.votes.sum_rating()
                }),
                content_type="application/json"
            )