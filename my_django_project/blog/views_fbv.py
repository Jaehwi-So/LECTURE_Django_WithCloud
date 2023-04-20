from django.shortcuts import render

from .models import Post
from django.views.generic import ListView


def post_list(request):
    posts = Post.objects.all().order_by('-pk')
    return render(
        request,
        'blog/post_list.html',
        {
            'posts': posts
        }
    )


def post_detail(request, pk):
    posts = Post.objects.get(pk=pk)
    return render(
        request,
        'blog/post_detail.html',
        {
            'post': posts
        }
    )