import logging
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from . forms import ContactForm

logger = logging.getLogger(__name__)  # ログ出力

class InquiryView(generic.FormView):
    """お問い合わせページ用ビュー"""

    form_class = ContactForm
    success_url = reverse_lazy('contact:thanks')
    template_name = 'contact/inquiry.html'

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class InquiryThanksView(generic.TemplateView):
    """お問い合わせありがとうございますページ用ビュー"""

    template_name = 'contact/thanks.html'