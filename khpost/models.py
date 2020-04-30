from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField


class GameTitleModel(models.Model):
    """ゲームタイトル名保存モデル"""

    name = models.CharField(verbose_name='ゲームタイトル名', max_length=255, unique=True)

    def __str__(self):
        return self.name


class TagModel(models.Model):
    """タグ名保存モデル"""

    name = models.CharField(verbose_name='タグ名', max_length=255, unique=True)

    def __str__(self):
        return self.name


class LikeModel(models.Model):
    """いいねモデル"""

    like_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='いいねしたユーザー',
    )

    def __str__(self):
        return str(self.like_user)

class BookMarkModel(models.Model):
    """ブックマークモデル"""

    bookmark_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='ブックマークしたユーザー',
    )

    def __str__(self):
        return str(self.bookmark_user)

class PostModel(models.Model):
    """記事投稿モデル"""

    title = models.CharField(verbose_name='タイトル', max_length=255)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='投稿者')
    game = models.ForeignKey(GameTitleModel, on_delete=models.PROTECT, verbose_name='ゲームタイトル')
    tags = models.ManyToManyField(TagModel, verbose_name='タグ', blank=True)
    content = RichTextUploadingField(verbose_name='本文', blank=True)

    likes = models.ManyToManyField(LikeModel, verbose_name='いいね', blank=True)
    bookmarks = models.ManyToManyField(BookMarkModel, verbose_name='ブックマーク', blank=True)
    is_public = models.IntegerField(verbose_name='公開設定', choices=((0, '非公開'), (1, '公開'),), default=0)

    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='最終更新日', auto_now=True)

    def __str__(self):
        return 'タイトル{}:投稿者{}'.format(self.title[:20], self.writer)

class CommentModel(models.Model):
    """記事に対するコメント投稿モデル"""

    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='コメントしたユーザー')
    text = models.TextField(verbose_name='本文', max_length=1000)
    target = models.ForeignKey(PostModel, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    def __str__(self):
        return self.text[:20]

class ReplyModel(models.Model):
    """コメントに対する返信投稿モデル"""

    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='返信したユーザー')
    text = models.TextField(verbose_name='本文', max_length=1000)
    target = models.ForeignKey(CommentModel, on_delete=models.CASCADE, verbose_name='対象コメント')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    def __str__(self):
        return self.text[:20]