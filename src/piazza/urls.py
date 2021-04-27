from django.contrib import admin
from django.urls import path, include
from posts.views import PostsViewSet, LikeDislikeViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', PostsViewSet)
router.register('like_dislike', LikeDislikeViewSet)
router.register('comment', CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('authorize/', include('users.urls')),
    path('', include(router.urls)),
    path('posts/', include('posts.urls'))
]
