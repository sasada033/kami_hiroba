from django import forms
from khpost.models import GameTitleModel
from .models import MyDeck


class CardSearchForm(forms.Form):
    """記事作成時に特定のカード名を記事内に挿入するための検索フォーム"""

    keyword_card = forms.CharField(
        label='キーワード', required=False, widget=forms.TextInput(attrs={'placeholder': 'キーワードを入力'})
    )
    gametitle_card = forms.ModelChoiceField(
        label='ゲーム選択', required=False, queryset=GameTitleModel.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['keyword_card'].widget.attrs['class'] = 'form-control card-search-keyword'
        self.fields['gametitle_card'].widget.attrs['class'] = 'form-control card-search-gametitle'
        self.fields['gametitle_card'].empty_label = 'ゲームを選択'


class DeckCreateForm(forms.ModelForm):
    """マイデッキ新規作成フォーム"""

    class Meta:
        model = MyDeck
        fields = (
            'title', 'game', 'kind', 'progress', 'label_first',
            'label_second', 'label_third', 'description', 'is_public',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'post-form-control'

