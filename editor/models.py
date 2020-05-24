from django.db import models
# from khpost.models import PostModel


class WeissSchwarz(models.Model):
    """ヴァイスシュヴァルツ カードデータ"""

    name = models.CharField(verbose_name='カード名', blank=True, max_length=100)
    num = models.CharField(verbose_name='カード番号', blank=True, max_length=30)
    title = models.CharField(verbose_name='収録弾', blank=True, max_length=100)
    side = models.CharField(
        verbose_name='サイド', blank=True, max_length=2, choices=(
            ('W', 'W'), ('S', 'S'),
        )
    )
    kind = models.CharField(
        verbose_name='種類', blank=True, max_length=20, choices=(
            ('キャラ', 'キャラ'), ('イベント', 'イベント'), ('クライマックス', 'クライマックス'),
        )
    )
    level = models.CharField(
        verbose_name='レベル', blank=True, max_length=2, choices=(
            ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'),
        )
    )
    color = models.CharField(
        verbose_name='色', blank=True, max_length=10, choices=(
            ('黄', '黄'), ('緑', '緑'), ('赤', '赤'), ('青', '青'),
        )
    )
    power = models.CharField(verbose_name='パワー', blank=True, max_length=10)
    soul = models.CharField(
        verbose_name='ソウル', blank=True, max_length=2, choices=(
            ('-', '-'), ('1', '1'), ('2', '2'), ('3', '3'),
        )
    )
    cost = models.CharField(verbose_name='コスト', blank=True, max_length=2)
    rarity = models.CharField(verbose_name='レアリティ', blank=True, max_length=30)
    trigger = models.CharField(verbose_name='トリガー', blank=True, max_length=30)
    identity = models.CharField(verbose_name='特徴', blank=True, max_length=50)
    flavor = models.TextField(verbose_name='フレーバー', blank=True, max_length=255)
    text = models.TextField(verbose_name='テキスト', blank=True, max_length=500)

    def __str__(self):
        return '{} - {}'.format(self.name, self.num)


# class CollectionCardData(models.Model):
#     """ポストモデルにカードデータリストを紐づけるための集約テーブル"""
#
#     weiss_schwarz = models.ManyToManyField(WeissSchwarz, verbose_name='ヴァイスシュヴァルツ', blank=True)
#
#     target = models.OneToOneField(PostModel, on_delete=models.CASCADE, verbose_name='対象記事')
#
#     def __str__(self):
#         return self.target
