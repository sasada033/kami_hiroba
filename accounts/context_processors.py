from django.shortcuts import get_object_or_404
from .models import UserProfile


def get_profile(request):

    context = {}

    if request.user.is_superuser:
        return context

    elif request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user_name=request.user)

        context.update({
            'profile': profile
        })

    return context
