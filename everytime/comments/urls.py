from django.urls import path
from . import views 
app_name = 'comments'

urlpatterns = [
    path('create/<int:post_id>/', views.comment_create, name='comment_create'),
    path('<int:comment_id>/like/', views.comment_like, name='comment_like'),
    path('delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('update/<int:comment_id>/', views.comment_update, name='comment_update'),
]