from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import WeissSchwarz, Yugioh


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
            'name', 'num', 'title', 'side', 'kind', 'level', 'color', 'power', 'soul', 'cost',
            'rarity', 'trigger', 'identity', 'flavor', 'text',
        ).distinct()[0:15]
        # Q()|...OR演算子, icontains...部分一致, distinct()...重複削除, [0:15]...先頭から15件まで取得
        # values_list()...json形式に対応できるようクエリセットをタプルで出力

        if results:
            data = {'queryset': list(results)}
        else:
            data = {'queryset': False}

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
