from django.shortcuts import render, get_object_or_404
from blog.models import Blog


def blog_index(request):
    return render(request, 'blog/index.html')


def blog_details_view(request):
	#blog_post = get_object_or_404(Blog, slug=slug)
	return render(request, 'blog/blog-details.html')