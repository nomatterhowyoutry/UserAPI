from django.db import models
from django.conf import settings
from django.db.models import Sum
from rest_framework.reverse import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def post(self):
        return self.get_queryset().filter(content_type__model='post').order_by('-posts__pub_date')


class LikeDislike(models.Model):
    class Meta:
        managed = True
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(verbose_name="Vote", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name="User",
                             on_delete=models.CASCADE
                             )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    objects = LikeDislikeManager()


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    votes = GenericRelation(LikeDislike, default=0, related_query_name='posts')

    def __str__(self):
        return str(self.user.username)


    def rating(self):
        return self.votes.sum_rating()

    def likes(self):
        return self.votes.likes().count()

    def dislikes(self):
        return self.votes.dislikes().count()

    @property
    def owner(self):
        return self.user

    def get_api_url(self, request=None):
        return reverse('postRud', kwargs={'pk' : self.pk}, request=request)