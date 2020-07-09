from django.contrib import admin
from .models import PostModel, GameTitleModel, TagModel, CommentModel

admin.site.register(PostModel)
admin.site.register(GameTitleModel)
admin.site.register(TagModel)
admin.site.register(CommentModel)
