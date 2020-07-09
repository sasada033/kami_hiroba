from django import forms
from khpost.models import GameTitleModel


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
