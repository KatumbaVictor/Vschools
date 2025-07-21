from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', blog_index, name='index'),
    path('blog-post/', blog_details_view, name="blog_detail"),
]
