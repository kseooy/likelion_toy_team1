from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', home, name='home'),
    path('list/', list, name='list'),
    path('create/', create, name='create'),
    path('detail/<int:id>/', detail, name='detail'),
    path('update/<int:id>/', update, name='update'),
    path('delete/<int:id>/', delete, name='delete'),
    path('post/<int:post_id>/like/', post_like, name='post_like'),
    path('search/', search, name='search'),
]