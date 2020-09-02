from django.contrib import messages
from django.contrib.auth import get_user_model  # Userモデルを汎用的に取得
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from .models import PostModel, TagModel, CommentModel
from .forms import PostCreateForm, TagCreateFormSet, CommentCreateForm, PostSearchForm
from editor.forms import CardSearchForm
from accounts.models import UserProfile


User = get_user_model()


class KhpostIndexView(TemplateView):
    """トップページビュー"""

    template_name = 'khpost/index.html'


class KhpostListView(ListView):
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


class KhpostDisplay(DetailView):
    """記事詳細ビュー"""

    model = PostModel
    template_name = 'khpost/khpost_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # コメントモデル取得
        comment_list = CommentModel.objects.select_related('writer',).filter(target=self.object)
        # いいねボタンの初期値設定
        if self.request.user in self.object.likes.all():
            like_active = True  # すでにいいねしている場合
        else:
            like_active = False

        context.update({
            'comment_list': comment_list,
            'like_active': like_active,
            'form': CommentCreateForm(),
        })
        return context


class KhpostComment(LoginRequiredMixin, SingleObjectMixin, FormView):
    """
    コメント投稿ビュー
    SingleObjectMixinによりDetailViewの機能を部分的に使用する。
    """

    form_class = CommentCreateForm
    model = PostModel
    template_name = 'khpost/khpost_detail.html'

    def post(self, request, *args, **kwargs):
        # コメントを紐づける対象の記事をインスタンス変数に格納
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.writer = self.request.user
        comment.target = self.object
        comment.save()
        messages.success(self.request, 'コメントを投稿しました。')
        return redirect('khpost:khpost_detail', pk=self.object.pk)


class KhpostDetailView(View):
    """
    記事詳細＋コメント投稿ビュー
    GET時には記事詳細ビューに処理を渡す。POST時にはコメント投稿ビューに処理を渡す。
    """

    def get(self, request, *args, **kwargs):
        view = KhpostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = KhpostComment.as_view()
        return view(request, *args, **kwargs)


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

    # 他のユーザーのアクセスを禁止
    if not request.user == instance.writer:
        raise PermissionDenied

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


class KhpostDeleteView(LoginRequiredMixin, DeleteView):
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


class UserProfileIndexView(DetailView):
    """ユーザーインデックスビュー(プロフィール＆記事一覧)"""

    model = User
    context_object_name = 'user_'
    template_name = 'khpost/profile.html'
    slug_field = 'username'  # urlの末尾に対応するusernameを割り当てる

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # PostModel,UserProfile のクエリセットを取得
        post_list = PostModel.objects.filter(
            writer=kwargs.get('object'), is_public=1
        ).select_related('writer', 'game').prefetch_related('tags', 'likes', 'bookmarks')

        profile = get_object_or_404(
            UserProfile.objects.prefetch_related('follower',), user_name=kwargs.get('object')
        )

        context.update({
            'post_list': post_list,
            'profile': profile
        })
        return context


class UserProfileDeckView(DetailView):
    """ユーザープロフィールデッキビュー(プロフィール＆デッキ一覧)"""

    model = User
    template_name = 'khpost/profile_followers.html'
    slug_field = 'username'  # urlの末尾に対応するusernameを割り当てる

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # UserProfile のクエリセットを取得
        context.update({
            'profile': get_object_or_404(
                UserProfile.objects.prefetch_related('follower', ), user_name=kwargs.get('object')
            )
        })
        return context


class UserProfileFollowersView(DetailView):
    """ユーザープロフィールフォロワービュー(プロフィール＆フォロワー一覧)"""

    model = User
    template_name = 'khpost/profile_followers.html'
    slug_field = 'username'  # urlの末尾に対応するusernameを割り当てる

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # UserProfile のクエリセットを取得
        context.update({
            'profile': get_object_or_404(
                UserProfile.objects.prefetch_related('follower', ), user_name=kwargs.get('object')
            )
        })
        return context


@login_required
def khpost_follow_view(request, pk):
    """ユーザーフォローボタン処理ビュー"""

    obj = get_object_or_404(UserProfile, pk=pk)
    status = request.GET.get('status')
    user = request.user

    if user in obj.follower.all():  # そのユーザーを既にフォロー中の場合
        if status:  # フォローボタン押下時(status=true)
            obj.follower.remove(user)  # フォローリストからそのユーザーを除外
            follow = False  # 非フォロー状態であることをテンプレートに伝達
        else:
            follow = True   # フォロー状態であることをテンプレートに伝達
    else:  # そのユーザーをまだフォローしていない場合
        if status:  # フォローボタン押下時(status=true)
            obj.follower.add(user)  # フォローリストにそのユーザーを追加
            follow = True  # フォロー状態であることをテンプレートに伝達
        else:
            follow = False  # 非フォロー状態であることをテンプレートに伝達

    data = {
        'followed': follow,
    }
    return JsonResponse(data)
