from django.contrib import admin
from .models import PostModel, GameTitleModel, TagModel, BookMarkModel, LikeModel, CommentModel, ReplyModel

admin.site.register(PostModel)
admin.site.register(GameTitleModel)
admin.site.register(TagModel)
admin.site.register(BookMarkModel)
admin.site.register(LikeModel)
admin.site.register(CommentModel)
admin.site.register(ReplyModel)