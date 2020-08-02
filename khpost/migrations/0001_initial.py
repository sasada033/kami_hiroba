# Generated by Django 3.0.8 on 2020-07-11 13:16

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameTitleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='ゲームタイトル名')),
            ],
        ),
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='タイトル')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='本文')),
                ('page_view', models.IntegerField(default=0, verbose_name='累計PV数')),
                ('is_public', models.IntegerField(choices=[(0, '非公開'), (1, '公開')], default=0, verbose_name='公開設定')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='最終更新日')),
                ('bookmarks', models.ManyToManyField(blank=True, related_name='post_bookmarks_set', to=settings.AUTH_USER_MODEL, verbose_name='ブックマーク')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='khpost.GameTitleModel', verbose_name='ゲームタイトル')),
                ('likes', models.ManyToManyField(blank=True, related_name='post_likes_set', to=settings.AUTH_USER_MODEL, verbose_name='いいね')),
            ],
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='タグ名')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyTrendModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekly_pv', models.IntegerField(default=0, verbose_name='7日間PV数')),
                ('path', models.URLField(blank=True, verbose_name='URL')),
                ('weekly_post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='khpost.PostModel')),
            ],
        ),
        migrations.AddField(
            model_name='postmodel',
            name='tags',
            field=models.ManyToManyField(blank=True, to='khpost.TagModel', verbose_name='タグ'),
        ),
        migrations.AddField(
            model_name='postmodel',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='post_writer_set', to=settings.AUTH_USER_MODEL, verbose_name='投稿者'),
        ),
        migrations.CreateModel(
            name='MonthlyTrendModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_pv', models.IntegerField(default=0, verbose_name='30日間PV数')),
                ('path', models.URLField(blank=True, verbose_name='URL')),
                ('monthly_post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='khpost.PostModel')),
            ],
        ),
        migrations.CreateModel(
            name='DailyTrendModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_pv', models.IntegerField(default=0, verbose_name='24時間PV数')),
                ('path', models.URLField(blank=True, verbose_name='URL')),
                ('daily_post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='khpost.PostModel')),
            ],
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1500, verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes_set', to=settings.AUTH_USER_MODEL, verbose_name='いいね')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='khpost.PostModel', verbose_name='対象記事')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_writer_set', to=settings.AUTH_USER_MODEL, verbose_name='コメントしたユーザー')),
            ],
        ),
    ]