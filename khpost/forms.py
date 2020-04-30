from django import forms
from .models import PostModel, CommentModel, ReplyModel

class PostCreateForm(forms.ModelForm):
    """記事新規作成フォーム"""

    class Meta:
        model = PostModel
        fields = ('title', 'game', 'tags', 'content', 'is_public')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

class CommentCreateForm(forms.ModelForm):
    """コメント投稿フォーム"""

    class Meta:
        model = CommentModel
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'ここに入力'})
        }

class ReplyCreateForm(forms.ModelForm):
    """コメント返信投稿フォーム"""

    class Meta:
        model = ReplyModel
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'ここに入力'})
        }
