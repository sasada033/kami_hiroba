from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    """ユーザーマネージャー（username欄をemailに変更）"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル(usernameとemail必須)"""

    email = models.EmailField(_('email address'), unique=True)

    username = models.SlugField(
        _('username'),
        max_length=32,
        unique=True,
        help_text='この項目は必須です。半角英数字および-_で3文字以上32文字以下にしてください。',
        validators=[MinLengthValidator(3)],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserProfile(models.Model):
    """ユーザープロフィールモデル"""

    user_name = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile_user_name_set'
    )
    follower = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name='フォロワー', blank=True, related_name='userprofile_follower_set'
    )
    handle = models.CharField(
        verbose_name='ハンドルネーム', max_length=32, blank=True
    )
    icon = models.ImageField(
        upload_to='media', verbose_name='アイコン', blank=True
    )
    description = models.TextField(
        verbose_name='自己紹介', max_length=1000, blank=True
    )
    location = models.CharField(
        verbose_name='居住地', max_length=100, blank=True
    )
    mysite = models.URLField(
        verbose_name='サイト/ブログ', blank=True
    )

    def __str__(self):
        return str(self.user_name)
