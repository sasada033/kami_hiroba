from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model  # Userモデルを汎用的に取得
from django.db.models import Q
from django.db import transaction
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import PostModel, TagModel
from .forms import PostCreateForm, TagCreateFormSet, CommentCreateForm, PostSearchForm
from editor.forms import CardSearchForm


User = get_user_model()


class KhpostIndexView(generic.TemplateView):
    """トップページビュー"""

    template_name = 'khpost/index.html'


class KhpostListView(generic.ListView):
    """記事一覧＋検索結果表示ビュー"""

    model = PostModel
    queryset = PostModel.objects.filter(is_public=1)  # 公開済の記事取得
    template_name = 'khpost/khpost_list.html'
    ordering = '-created_at'
    paginate_by = 3

    def get_queryset(self):
        queryset = \
            super().get_queryset().select_related('writer', 'game').prefetch_related('tags', 'likes', 'bookmarks')
        form = PostSearchForm(self.request.GET or None)

        if form.is_valid():
            key_word = form.cleaned_data.get('key_word')  # 検索値取得
            gametitle = form.cleaned_data.get('gametitle')
            if key_word:
                queryset = queryset.filter(
                    Q(
                        title__icontains=key_word
                    ) | Q(
                        game__name__icontains=key_word
                    ) | Q(
                        tags__name__icontains=key_word
                    ) | Q(
                        content__icontains=key_word
                    )
                ).distinct()  # Q()|...OR, icontains...部分一致
            if gametitle:
                queryset = queryset.filter(game__name=gametitle)

        return queryset


def khpost_detail(request, pk):
    """記事詳細＋コメント機能＋いいね機能ビュー"""

    # 詳細記事取得
    article = \
        get_object_or_404(
            PostModel.objects.select_related('writer', 'game').prefetch_related('tags', 'likes', 'bookmarks'), pk=pk
        )

    # コメントフォーム生成
    form = CommentCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():  # request.POST時の処理
        comment = form.save(commit=False)
        comment.writer = request.user
        comment.target = article
        comment.save()
        return redirect('khpost:khpost_detail', pk=pk)

    # いいねボタンの初期値設定
    if request.user in article.likes.all():
        like_active = True  # すでにいいねしている場合
    else:
        like_active = False

    context = {
        'postmodel': article,
        'form': form,
        'like_active': like_active
    }
    return render(request, 'khpost/khpost_detail.html', context)


@login_required
def khpost_create_view(request):
    """記事作成ビュー（記事フォーム＆タグフォームセット＆カード検索フォーム）"""

    post_form = PostCreateForm(request.POST or None)
    context = {
        'post_form': post_form,
    }

    if request.method == 'POST' and post_form.is_valid():
        new_post = post_form.save(commit=False)
        tag_form = TagCreateFormSet(request.POST)

        if tag_form.is_valid():
            with transaction.atomic():  # with節内をトランザクションに含める(エラー時にDBが汚れるのを防止)
                # PostModelを保存  # commit=Falseでuserを登録
                new_post.writer = request.user
                new_post.save()

                # TagModelを手動で保存するための準備(save()を使わない)
                # たったいまsaveしたレコードをPostModelから取得
                p = get_object_or_404(
                    PostModel.objects.select_related('writer', 'game').prefetch_related('tags', 'likes', 'bookmarks'),
                    id=new_post.id
                )

                # たったいま入力されたタグのリスト  # if dataでNull値を回避
                input_tag = [data.get('name') for data in tag_form.cleaned_data if data]

                # input_tagをadd()でPostModelに紐づける
                # 既にTagModelにinput_tagが登録されている場合はget、そうでない場合はcreate処理(get_or_create())
                if input_tag:
                    for nt in input_tag:
                        obj, created = TagModel.objects.get_or_create(name=nt)  # createdには真偽値が入る
                        p.tags.add(obj)

                # リダイレクト後のメッセージ
                messages.success(request, '記事を保存しました。')
                return redirect('khpost:khpost_list')
        else:
            context.update({
                'tag_form': tag_form,
            })  # エラー時

    else:  # request.GET時
        context.update({
            'tag_form': TagCreateFormSet(queryset=TagModel.objects.none()),  # 空のフォームセットを渡す
            'card_form': CardSearchForm(),
        })

    return render(request, 'khpost/khpost_create.html', context)


@login_required
def khpost_update_view(request, pk):
    """記事更新ビュー"""

    # post_formの初期値
    instance = get_object_or_404(
        PostModel.objects.select_related('writer', 'game').prefetch_related('tags', 'likes', 'bookmarks'), pk=pk
    )
    post_form = PostCreateForm(request.POST or None, instance=instance)
    context = {
        'post_form': post_form,
    }

    if request.method == 'POST' and post_form.is_valid():
        new_post = post_form.save(commit=False)
        tag_form = TagCreateFormSet(request.POST)  # 登録処理に渡されたタグ

        if tag_form.is_valid():
            with transaction.atomic():  # with節内をトランザクションに含める(エラー時にDBが汚れるのを防止)
                # PostModelを保存
                new_post.save()

                # TagModelを手動で保存するための準備(save()を使わない)
                current_tag = list(instance.tags.values_list('name', flat=True))  # 現在DBに登録されているタグのリスト
                input_tag = [data.get('name') for data in tag_form.cleaned_data if data]  # たったいま入力されたタグのリスト
                old_tag = list(set(current_tag) - set(input_tag))  # 使わなくなったタグのリスト
                new_tag = list(set(input_tag) - set(current_tag))  # 新規追加されたタグのリスト

                # PostModelのtagsフィールドからold_tagを除外し、同フィールドにnew_tagを追加
                # old_tagの紐づけをremove()で解除（TagModelからは削除されない）
                if old_tag:
                    for ot in old_tag:
                        instance.tags.remove(get_object_or_404(TagModel, name=ot))
                # new_tagをadd()で紐づける
                # 既にTagModelにnew_tagが登録されている場合はget、そうでない場合はcreate処理(get_or_create())
                if new_tag:
                    for nt in new_tag:
                        obj, created = TagModel.objects.get_or_create(name=nt)
                        instance.tags.add(obj)

                # リダイレクト後のメッセージ
                messages.success(request, '記事を更新しました。')
                return redirect('khpost:khpost_list')
        else:
            context.update({
                'tag_form': tag_form,
            })  # エラー時

    else:  # request.GET時
        context.update({
            'tag_form': TagCreateFormSet(queryset=instance.tags.all()),  # PostModelに紐づいたTagModelを取得
            'card_form': CardSearchForm(),
        })

    return render(request, 'khpost/khpost_update.html', context)


class KhpostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """記事削除ビュー"""

    model = PostModel
    template_name = 'khpost/khpost_delete.html'
    success_url = reverse_lazy('khpost:khpost_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '記事を削除しました。')
        return super().delete(request, *args, **kwargs)


@login_required
def khpost_like_view(request, pk):
    """いいねボタン処理ビュー"""

    obj = get_object_or_404(PostModel, pk=pk)
    status = request.GET.get('status')
    user = request.user

    if user in obj.likes.all():  # ユーザーが既にいいねしていた場合
        if status:  # いいねボタン押下時(status=true)
            obj.likes.remove(user)  # いいねリストからユーザーを除外
            liked = False  # 非いいね状態であることをテンプレートに伝達
        else:
            liked = True   # いいね状態であることをテンプレートに伝達
    else:  # ユーザーがまだいいねしていない場合
        if status:  # いいねボタン押下時(status=true)
            obj.likes.add(user)  # いいねリストにユーザーを追加
            liked = True  # いいね状態であることをテンプレートに伝達
        else:
            liked = False  # 非いいね状態であることをテンプレートに伝達

    data = {
        'liked': liked,
    }
    return JsonResponse(data)
