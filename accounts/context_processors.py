from django.shortcuts import get_object_or_404
from .models import UserProfile
from khpost.models import PostModel


def get_profile(request):

    context = {}

    if request.user.is_superuser:
        return context

    elif request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user_name=request.user)
        post_count = PostModel.objects.filter(writer=request.user, is_public=1).count()

        context.update({
            'profile': profile,
            'post_count': post_count
        })

    return context
