from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    NewsCreateView, 
    ArticleCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    path('', PostListView.as_view(), name='news_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post'),
    
    # Новости
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
    
    # Статьи
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', PostUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDeleteView.as_view(), name='article_delete'),
]
