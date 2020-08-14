from django import template
from django.template.defaultfilters import stringfilter
from khpost.forms import PostSearchForm


register = template.Library()


@register.simple_tag
def url_replace(request, field, value):  # GETパラメータを一部置き換える

    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()


@register.filter(is_safe=True)
@stringfilter
def split_timesince(value, delimiter=None):  # timesince を分割してシンプルに表示する

    return value.split(delimiter)[0]


@register.inclusion_tag('khpost/search_form.html')
def create_search_form(request):

    form = PostSearchForm(request.GET or None)
    return {'form': form}
