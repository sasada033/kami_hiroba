from django.db import models
from django.conf import settings
from khpost.models import GameTitleModel
from storage.models import Yugioh, WeissSchwarz
# from taggit.managers import TaggableManager


class MyDeck(models.Model):
    """ユーザーに紐づくデッキリストモデル"""

    title = models.CharField(
        verbose_name='デッキタイトル', default='マイデッキ', max_length=40
    )
    holder = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='デッキ所持者'
    )
    game = models.ForeignKey(
        GameTitleModel, on_delete=models.PROTECT, verbose_name='ゲームタイトル'
    )
    kind = models.IntegerField(
        verbose_name='種類', default=0, choices=(
            (0, 'デッキ'),
            (1, 'メモ')
        )
    )
    # tags = TaggableManager(
    #     blank=True
    # )
    progress = models.IntegerField(
        verbose_name='完成度', default=0, choices=(
            (0, '1'),
            (1, '2'),
            (2, '3'),
            (3, '4'),
            (4, '5')
        )
    )
    label_first = models.CharField(
        verbose_name='ラベル１', default='メインデッキ', blank=True, max_length=20
    )
    label_second = models.CharField(
        verbose_name='ラベル２', default='エクストラデッキ', blank=True, max_length=20
    )
    label_third = models.CharField(
        verbose_name='ラベル３', default='サイドデッキ', blank=True, max_length=20
    )
    description = models.TextField(
        verbose_name='説明', blank=True, max_length=500
    )
    is_public = models.IntegerField(
        verbose_name='公開設定', choices=(
            (0, '非公開'), (1, '公開')
        ), default=0
    )
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='最終更新日', auto_now=True)

    def __str__(self):
        return '{} by {}'.format(self.title, self.holder)


class WeissSchwarzDeckContent(models.Model):
    """ヴァイスシュヴァルツ用 MyDeckモデルの子モデル"""

    target = models.ForeignKey(
        MyDeck, on_delete=models.CASCADE
    )
    number_of_card = models.IntegerField(
        verbose_name='枚数', default=1
    )
    label = models.IntegerField(
        verbose_name='ラベル', choices=(
            (0, 'ラベル１'), (1, 'ラベル２'), (2, 'ラベル３')
        ), default=0
    )
    weiss_schwarz = models.ForeignKey(
        WeissSchwarz, on_delete=models.PROTECT, verbose_name='ヴァイスシュヴァルツ', blank=True
    )

    def __str__(self):
        return str(self.target)


class YugiohDeckContent(models.Model):
    """遊戯王用 MyDeckモデルの子モデル"""

    target = models.ForeignKey(
        MyDeck, on_delete=models.CASCADE
    )
    number_of_card = models.IntegerField(
        verbose_name='枚数', default=1
    )
    label = models.IntegerField(
        verbose_name='ラベル', choices=(
            (0, 'ラベル１'), (1, 'ラベル２'), (2, 'ラベル３')
        ), default=0
    )
    yugioh = models.ForeignKey(
        Yugioh, on_delete=models.PROTECT, verbose_name='遊戯王', blank=True
    )

    def __str__(self):
        return str(self.target)
