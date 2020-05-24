from django import forms
from django.contrib.auth import get_user_model
from .models import PostModel, TagModel, GameTitleModel, CommentModel


User = get_user_model()  # プロジェクトのユーザーモデルを取得


class PostCreateForm(forms.ModelForm):
    """記事新規作成フォーム"""

    class Meta:
        model = PostModel
        fields = ('title', 'game', 'content', 'is_public')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'post-form-control'

        self.fields['content'].widget.attrs['id'] = 'post-create-form'


class TagCreateForm(forms.ModelForm):
    """タグ作成フォーム"""

    class Meta:
        model = TagModel
        fields = ('name',)


TagCreateFormSet = forms.modelformset_factory(
    TagModel, form=TagCreateForm, extra=5, max_num=5, can_delete=False,
)


class CommentCreateForm(forms.ModelForm):
    """コメント投稿フォーム"""

    class Meta:
        model = CommentModel
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'ここに入力'})
        }


class PostSearchForm(forms.Form):
    """記事検索フォーム"""

    keyword = forms.CharField(
        label='キーワード', required=False, widget=forms.TextInput(attrs={'placeholder': 'キーワードを入力'})
    )
    gametitle = forms.ModelChoiceField(
        label='ゲームタイトルの選択', required=False, queryset=GameTitleModel.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['keyword'].widget.attrs['class'] = 'form-control post-keyword'
        self.fields['gametitle'].widget.attrs['class'] = 'form-control post-gametitle'
        self.fields['gametitle'].empty_label = 'すべてのタイトル'
