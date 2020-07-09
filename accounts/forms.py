from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import UserProfile
from allauth.account.forms import SignupForm


User = get_user_model()


class MyUserChangeForm(UserChangeForm):
    """（管理画面用 form=MyUserChangeForm admin.py）"""

    class Meta:
        model = User
        fields = '__all__'


class MyCustomSignupForm(SignupForm):
    """サインアップフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = forms.SlugField(
            label='ユーザー名',
            required=True,
            help_text='この項目は必須です。半角英数字および_, -のみを用いて3文字以上32文字以下で入力してください。',
        )

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super().save(request)
        # Add your own processing here.
        profile = UserProfile(user_name=user)  # UserProfileモデルをサインアップ時に自動で追加
        profile.save()
        # You must return the original result.
        return user


class UserProfileForm(forms.ModelForm):
    """ユーザープロフィール更新フォーム"""

    class Meta:
        model = UserProfile
        exclude = ('user_name',)


class DeactivateForm(forms.ModelForm):
    """退会処理フォーム"""

    class Meta:
        model = User
        fields = ('is_active',)

    deactivate_password = forms.CharField(
        label='パスワード',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'パスワードを入力'}))

    def __init__(self, *args, **kwargs):
        kwargs['initial'] = {'is_active': False}
        self.user = kwargs.get('instance', None)

        super().__init__(*args, **kwargs)
        self.fields['is_active'].label = 'アカウントを削除する'

    def clean_deactivate_password(self):
        password = self.cleaned_data['deactivate_password']
        if not check_password(password, self.user.password):
            raise forms.ValidationError('パスワードが正しくありません。')
        return password

    def clean_is_active(self):
        is_active = not(self.cleaned_data['is_active'])
        if is_active:
            raise forms.ValidationError('退会を完了するにはチェックを入れてください。')
        return is_active
