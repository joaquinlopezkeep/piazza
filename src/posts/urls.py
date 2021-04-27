from django.urls import path
from . import views
urlpatterns = [
    path('topic/<str:topic>/', views.all_by_topic),
    path('topic/<str:topic>/<str:status>/', views.post_by_topic_status),
    path('most-active/<str:topic>/', views.most_active_topic),
    path('most-active/<str:topic>/<str:status>/',
         views.most_active_topic_status),

]
