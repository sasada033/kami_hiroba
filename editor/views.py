from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from storage.models import WeissSchwarz, Yugioh
from .forms import CardSearchForm, DeckCreateForm


@login_required
def card_search_view(request):
    """記事作成時のカード検索ビュー"""

    gametitle = request.GET.get('gametitle')
    keyword = request.GET.get('keyword')

    titles = {
        'weissschwarz': 'ヴァイスシュヴァルツ',
        'yugioh': '遊戯王',
    }

    if gametitle == titles['weissschwarz']:
        """ヴァイスシュヴァルツ検索"""

        results = WeissSchwarz.objects.filter(
            Q(
                name__icontains=keyword
            ) | Q(
                num__icontains=keyword
            ) | Q(
                title__icontains=keyword
            ) | Q(
                text__icontains=keyword
            )
        ).values_list(
            'id', 'name', 'num', 'title', 'side', 'kind', 'level', 'color', 'power', 'soul', 'cost',
            'rarity', 'trigger', 'identity', 'flavor', 'text',
        ).distinct()[0:15]
        # Q()|...OR演算子, icontains...部分一致, distinct()...重複削除, [0:15]...先頭から15件まで取得
        # values_list()...json形式に対応できるようクエリセットをタプルで出力

        if results:
            pk_list = []
            queryset = []
            for result in list(results):
                pk_list.append(list(result)[0])
                queryset.append(list(result)[1:])
            data = {
                'queryset': queryset,
                'pk': pk_list
            }
        else:
            data = {
                'queryset': None,
                'pk': []
            }

        return JsonResponse(data)

    elif gametitle == titles['yugioh']:
        """遊戯王検索"""

        results = Yugioh.objects.filter(
            Q(
                name__icontains=keyword
            ) | Q(
                reading__icontains=keyword
            ) | Q(
                text__icontains=keyword
            )
        ).values_list(
            'name', 'reading', 'element', 'level', 'species', 'attack', 'defence', 'text',
        ).distinct()[0:15]

        if results:
            data = {'queryset': list(results)}
        else:
            data = {'queryset': False}

        return JsonResponse(data)

    else:
        data = {'queryset': False}
        return JsonResponse(data)


@login_required
def deck_create_view(request):
    """マイデッキ作成ビュー"""

    deck_form = DeckCreateForm(request.POST or None)
    context = {
        'deck_form': deck_form,
        'card_form': CardSearchForm(),
    }

    if request.method == 'POST' and deck_form.is_valid():

        new_deck = deck_form.save(commit=False)
        new_deck.holder = request.user
        new_deck.save()


    #         with transaction.atomic():  # with節内をトランザクションに含める(エラー時にDBが汚れるのを防止)
    #             # PostModelを保存  # commit=Falseでuserを登録
    #             new_post.writer = request.user
    #             new_post.save()
    #
    #             # TagModelを手動で保存するための準備(save()を使わない)
    #             # たったいまsaveしたレコードをPostModelから取得
    #             p = get_object_or_404(
    #                 PostModel.objects.select_related('writer', 'game').prefetch_related('tags', 'likes', 'bookmarks'),
    #                 id=new_post.id
    #             )
    #
    #             # たったいま入力されたタグのリスト  # if dataでNull値を回避
    #             input_tag = [data.get('name') for data in tag_form.cleaned_data if data]
    #
    #             # input_tagをadd()でPostModelに紐づける
    #             # 既にTagModelにinput_tagが登録されている場合はget、そうでない場合はcreate処理(get_or_create())
    #             if input_tag:
    #                 for nt in input_tag:
    #                     obj, created = TagModel.objects.get_or_create(name=nt)  # createdには真偽値が入る
    #                     p.tags.add(obj)
    #
    #             # リダイレクト後のメッセージ
    #             messages.success(request, '記事を保存しました。')
    #             return redirect('khpost:khpost_list')
    #     else:
    #         context.update({
    #             'tag_form': tag_form,
    #         })  # エラー時
    #
    # else:  # request.GET時
    #     context.update({
    #         'tag_form': TagCreateFormSet(queryset=TagModel.objects.none()),  # 空のフォームセットを渡す
    #         'card_form': CardSearchForm(),
    #     })

    return render(request, 'editor/deck_create.html', context)


