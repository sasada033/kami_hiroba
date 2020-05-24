from accounts.models import settings
from django.db import models

class Hiroba(models.Model):
    """記事モデル"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    content = models.TextField(verbose_name='本文', blank=True, null=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='アドいいね', blank=True, related_name='likes')
    photo = models.ImageField(verbose_name='画像', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)


    class Meta:
        verbose_name_plural = '記事モデル'

    def __str__(self):
        return self.title