from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    dislikes = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'title',
            'content',
            'rating',
            'likes',
            'dislikes',
            'user',
            'timestamp',
        ]
        read_only_fields = [
            'id',
            'user',
        ]

    def validate_title(self, title):
        query = Post.objects.filter(title__iexact=title)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError("This title has already been used.")
        return title

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def get_likes(self, obj):
        return obj.likes()

    def get_dislikes(self, obj):
        return obj.dislikes()

    def get_rating(self, obj):
        return obj.rating()