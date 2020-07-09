from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import UserProfile
from .forms import UserProfileForm, DeactivateForm


User = get_user_model()


@login_required
def user_profile_change(request):
    """ユーザープロフィール更新ビュー"""

    profile = get_object_or_404(UserProfile, user_name=request.user)
    form = UserProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        new_icon = request.FILES.get('icon')  # 画像データは更新があったときのみ値を保存
        if new_icon:
            profile.icon = new_icon
        profile.save()
        messages.success(request, 'プロフィールを更新しました。')
        return redirect('accounts:settings_profile')

    context = {
        'form': form,
    }
    return render(request, 'accounts/profile_change.html', context)


class DeactivateView(LoginRequiredMixin, generic.FormView):
    """退会処理ビュー（要パスワード入力）"""

    form_class = DeactivateForm
    template_name = 'accounts/deactivate.html'
    success_url = reverse_lazy('accounts:deactivate_done')

    def form_valid(self, form):
        deactivate_user = form.save(commit=False)
        deactivate_user.is_active = False
        deactivate_user.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs


class DeactivateDoneView(generic.TemplateView):
    """退会処理完了ビュー"""

    template_name = 'accounts/deactivate_done.html'


# """エラーコード"""

# class UserProfileChangeView(LoginRequiredMixin, generic.FormView):
#     """ユーザープロフィール更新ビュー"""
#
#     form_class = UserProfileForm
#     template_name = 'accounts/profile_change.html'
#     success_url = reverse_lazy('accounts:settings_profile')
#
#     def form_valid(self, form):
#         form.save()
#         messages.success(self.request, 'プロフィールを更新しました。')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         messages.error(self.request, '入力された内容に不備があります。ご確認下さい。')
#         return super().form_invalid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         profile = get_object_or_404(UserProfile, user_name=self.request.user)
#         context['form'] = UserProfileForm(self.request.POST or None, instance=profile)
#         return context
