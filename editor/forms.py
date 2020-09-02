from django import forms
from .models import MyDeck
from khpost.forms import GAME_TITLES


class CardSearchForm(forms.Form):
    """記事作成時に特定のカード名を記事内に挿入するための検索フォーム"""

    keyword_card = forms.CharField(
        label='キーワード', required=False, widget=forms.TextInput(attrs={'placeholder': 'キーワードを入力'})
    )
    gametitle_card = forms.ChoiceField(
        label='ゲーム選択', required=False, choices=GAME_TITLES,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['keyword_card'].widget.attrs['class'] = 'form-control card-search-keyword'
        self.fields['gametitle_card'].widget.attrs['class'] = 'form-control card-search-gametitle'


class DeckCreateCheckForm(forms.ModelForm):
    """マイデッキ作成時にタイトル選択するためのフォーム"""

    gametitle_card = forms.ChoiceField(
        label='ゲーム選択', choices=GAME_TITLES,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gametitle_card'].widget.attrs['class'] = 'form-control card-search-gametitle'


class DeckCreateForm(forms.ModelForm):
    """マイデッキ新規作成フォーム"""

    class Meta:
        model = MyDeck
        fields = (
            'title', 'game', 'label_first', 'label_second', 'label_third', 'description', 'is_public',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'post-form-control'
