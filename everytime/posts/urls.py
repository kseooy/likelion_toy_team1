from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', home, name='home'),
    path('list/', list, name='post_list'),  # post_list로 함수명 수정
    path('create/', create, name='create'),
    path('detail/<int:id>/', detail, name='detail'),
    path('update/<int:id>/', update, name='update'),
    path('delete/<int:id>/', delete, name='delete'),
    path('post/<int:post_id>/like/', post_like, name='post_like'),
    path('post/<int:post_id>/bookmark/', post_bookmark, name='post_bookmark'),
    path('search/', search, name='search'),
    path('search/delete/', delete_search_keyword, name='delete_search_keyword'),
    path('archive/', archive, name='archive'),
]