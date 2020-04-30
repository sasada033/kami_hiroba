import logging

from django.urls import reverse_lazy

from django.views import generic

from .forms import InquiryForm, HirobaCreateForm

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Hiroba

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('hiroba:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class HirobaListView(LoginRequiredMixin, generic.ListView):
    model = Hiroba
    template_name = 'hiroba_list.html'
    paginate_by = 3

    def get_queryset(self):
        hiroba_articles = Hiroba.objects.filter(user=self.request.user).order_by('-created_at')
        return hiroba_articles

class HirobaDetailView(LoginRequiredMixin, generic.DetailView):
    model = Hiroba
    template_name = 'hiroba_detail.html'

class HirobaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Hiroba
    template_name = 'hiroba_create.html'
    form_class = HirobaCreateForm
    success_url = reverse_lazy('hiroba:hiroba_list')

    def form_valid(self, form):
        hiroba = form.save(commit=False)
        hiroba.user = self.request.user
        hiroba.save()
        messages.success(self.request, '記事を投稿しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "記事の投稿に失敗しました。")
        return super().form_invalid(form)

class HirobaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Hiroba
    template_name = 'hiroba_update.html'
    form_class = HirobaCreateForm

    def get_success_url(self):
        return reverse_lazy('hiroba:hiroba_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '記事を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "記事の更新に失敗しました。")
        return super().form_invalid(form)

class HirobaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Hiroba
    template_name = 'hiroba_delete.html'
    success_url = reverse_lazy('hiroba:hiroba_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "記事を削除しました。")
        return super().delete(request, *args, **kwargs)

