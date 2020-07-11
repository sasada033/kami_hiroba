# Generated by Django 3.0.8 on 2020-07-11 13:16

import accounts.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.SlugField(error_messages={'unique': 'A user with that username already exists.'}, help_text='この項目は必須です。半角英数字および-_で3文字以上15文字以下にしてください。', max_length=15, unique=True, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('block_user', models.ManyToManyField(blank=True, related_name='_user_block_user_+', to=settings.AUTH_USER_MODEL, verbose_name='blocking user')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(blank=True, max_length=50, verbose_name='ハンドルネーム')),
                ('icon', models.ImageField(blank=True, upload_to='media', verbose_name='アイコン')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='自己紹介')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='居住地')),
                ('mysite', models.URLField(blank=True, verbose_name='サイト/ブログ')),
                ('follower', models.ManyToManyField(blank=True, related_name='profile_follower_set', to=settings.AUTH_USER_MODEL, verbose_name='フォロワー')),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
