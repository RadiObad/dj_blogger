from django.urls import path
from .views import (
    home,
    # PostListView,
    post_detail,
    post_share,
    # PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', home, name='blog-home'),
    # path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post-detail'),
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<slug:slug>/share/', post_share, name='post_share'),
    path('about/', views.about, name='blog-about'),

]