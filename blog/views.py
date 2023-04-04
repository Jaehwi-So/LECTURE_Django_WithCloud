from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post, Category, Tag


# CBV
class PostList(ListView):
    model = Post
    ordering = '-pk'

    #오버라이딩, 추가하고 싶은 요소를 context Dic에 담아 리턴해주면 보낼 수 있음
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        #미분류 카테고리 개수
        context['no_category_count'] = Post.objects.filter(category=None).count()
        return context


class PostDetail(DetailView):
    model = Post



#FBV
def categories_page(request, slug) :
    if slug == 'no-category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug = slug)
        post_list = Post.objects.filter(category=category)

    #카테고리 리스트, 현재 카테고리, 속하는 포스트, 카테고리없는 포스트 수
    context = {
        'category': category,
        'categories': Category.objects.all(),
        'post_list': post_list,
        'no_category_count' : Post.objects.filter(category=None).count()
    }
    return render(request, 'blog/post_list.html', context)


def tag_page(request, slug) :
    tag = Tag.objects.get(slug = slug)
    # 태그 리스트의 엘레멘트가 포함된 포스트를 모두 찾아야 함
    # post_list = Post.objects.filter(tag=tag)
    post_list = tag.post_set.all()

    context = {
        'tag': tag,
        'categories': Category.objects.all(),
        'post_list': post_list,
        'no_category_count' : Post.objects.filter(category=None).count()
    }
    return render(request, 'blog/post_list.html', context)


