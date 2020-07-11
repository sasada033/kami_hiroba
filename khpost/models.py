from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField


class GameTitleModel(models.Model):
    """ゲームタイトル名保存モデル"""

    name = models.CharField(verbose_name='ゲームタイトル名', max_length=50, unique=True)

    def __str__(self):
        return self.name


class TagModel(models.Model):
    """タグ名保存モデル"""

    name = models.CharField(verbose_name='タグ名', max_length=50, blank=True)

    def __str__(self):
        return self.name


class PostModel(models.Model):
    """記事投稿モデル"""

    title = models.CharField(
        verbose_name='タイトル', max_length=150
    )
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='投稿者', related_name='post_writer_set'
    )
    game = models.ForeignKey(
        GameTitleModel, on_delete=models.PROTECT, verbose_name='ゲームタイトル'
    )
    tags = models.ManyToManyField(
        TagModel, verbose_name='タグ', blank=True
    )
    content = RichTextUploadingField(
        verbose_name='本文', blank=True
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name='いいね', blank=True, related_name='post_likes_set'
    )
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name='ブックマーク', blank=True, related_name='post_bookmarks_set'
    )
    page_view = models.IntegerField(
        verbose_name='累計PV数', default=0
    )
    is_public = models.IntegerField(
        verbose_name='公開設定', choices=((0, '非公開'), (1, '公開'),), default=0
    )
    created_at = models.DateTimeField(
        verbose_name='作成日', auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='最終更新日', auto_now=True
    )

    def __str__(self):
        return 'タイトル{}:投稿者{}'.format(self.title[:20], self.writer)


class CommentModel(models.Model):
    """記事に対するコメント投稿モデル"""

    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='コメントしたユーザー',
        related_name='comment_writer_set'
    )
    text = models.TextField(
        verbose_name='本文', max_length=1500
    )
    target = models.ForeignKey(
        PostModel, on_delete=models.CASCADE, verbose_name='対象記事'
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name='いいね', blank=True, related_name='comment_likes_set'
    )
    created_at = models.DateTimeField(
        verbose_name='作成日', auto_now_add=True
    )

    def __str__(self):
        return '{}さんの{}へのコメント'.format(self.writer, self.target)


class DailyTrendModel(models.Model):
    """24時間の人気記事モデル"""

    daily_post = models.OneToOneField(
        PostModel, on_delete=models.CASCADE
    )
    daily_pv = models.IntegerField(
        verbose_name='24時間PV数', default=0
    )
    path = models.URLField(
        verbose_name='URL', blank=True
    )

    def __str__(self):
        return '{}/{}views'.format(self.daily_post, self.daily_pv)


class WeeklyTrendModel(models.Model):
    """7日間の人気記事モデル"""

    weekly_post = models.OneToOneField(
        PostModel, on_delete=models.CASCADE
    )
    weekly_pv = models.IntegerField(
        verbose_name='7日間PV数', default=0
    )
    path = models.URLField(
        verbose_name='URL', blank=True
    )

    def __str__(self):
        return '{}/{}views'.format(self.weekly_post, self.weekly_pv)


class MonthlyTrendModel(models.Model):
    """30日間の人気記事モデル"""

    monthly_post = models.OneToOneField(
        PostModel, on_delete=models.CASCADE
    )
    monthly_pv = models.IntegerField(
        verbose_name='30日間PV数', default=0
    )
    path = models.URLField(
        verbose_name='URL', blank=True
    )

    def __str__(self):
        return '{}/{}views'.format(self.monthly_post, self.monthly_pv)
