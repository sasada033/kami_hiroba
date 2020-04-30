from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import GameTitleModel, TagModel, LikeModel, BookMarkModel, PostModel, CommentModel
from .forms import PostCreateForm, CommentCreateForm

class KhpostIndexView(generic.TemplateView):
    """トップページビュー"""

    template_name = 'khpost/index.html'

class KhpostListView(generic.ListView):
    """記事一覧ビュー"""

    model = PostModel
    template_name = 'khpost/khpost_list.html'
    ordering = '-created_at'
    paginate_by = 3

    def get_queryset(self):
        public_articles = PostModel.objects.filter(is_public=1)
        return public_articles

class KhpostDetailView(generic.DetailView):
    """記事詳細＋コメント機能ビュー"""

    model = PostModel
    template_name = 'khpost/khpost_detail.html'

class KhpostCreateView(LoginRequiredMixin, generic.CreateView):
    """記事作成ビュー"""

    model = PostModel
    form_class = PostCreateForm
    template_name = 'khpost/khpost_create.html'
    success_url = reverse_lazy('khpost:khpost_list')

    def form_valid(self, form):
        postmodel = form.save(commit=False)
        postmodel.writer = self.request.user  # フォームに表示したくない値の取得
        postmodel.save()
        messages.success(self.request, '記事を保存しました。')  # リダイレクト後のメッセージ
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, '入力された内容に不備があります。ご確認下さい。')
        return super().form_invalid(form)

class KhpostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """記事更新ビュー"""

    model = PostModel
    form_class = PostCreateForm
    template_name = 'khpost/khpost_update.html'

    def get_success_url(self):
        return reverse_lazy('khpost:khpost_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '記事を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '入力された内容に不備があります。ご確認下さい。')
        return super().form_invalid(form)

class KhpostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """記事削除ページ用ビュー"""

    model = PostModel
    template_name = 'khpost/khpost_delete.html'
    success_url = reverse_lazy('khpost:khpost_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, '記事を削除しました。')
        return super().delete(request, *args, **kwargs)
