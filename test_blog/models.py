from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    order_to_sent = models.BooleanField('Разослать уведомления?', default=False)
    already_sent = models.BooleanField('Уведомления разосланы', default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('post_page', args=[self.author.username, self.pk])
        return url

class UserProfile(models.Model):
    from_follow = models.ForeignKey('auth.User', related_name='follow_set', on_delete=models.CASCADE)
    to_follow = models.ForeignKey('auth.User', related_name='to_follow_set', on_delete=models.CASCADE)
    noted = models.ManyToManyField(Post, blank=True, verbose_name='Прочитано', related_name='noted')

    def __unicode__(self):
        return u'%s, %s' % (
        self.from_follow.username,
        self.to_follow.username
        )

    class Meta:
        unique_together = (('to_follow', 'from_follow'), )