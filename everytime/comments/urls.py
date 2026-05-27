from django.urls import *
from .views import comment_create, comment_like

app_name = 'comments'

urlpatterns = [
    path('create/<int:post_id>/', comment_create, name='comment_create'),
    path('<int:comment_id>/like/', comment_like, name='comment_like'),
]