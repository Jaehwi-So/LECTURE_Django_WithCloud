from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView

#CBV

## 포스팅 리스트
class PostList(ListView):
    model = Post
    ordering = '-pk'

    # render시 아래의 별도 설정이 없을 시 경로는 post_list.html, 모델은 자동으로 post_list로 할당됨
    template_name = 'blog/post_list.html'   #템플릿 설정

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()
        return context

## 포스팅 상세보기
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


## 포스팅 등록
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tags']


    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog')

## 포스팅 수정
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tags']
    template_name = 'blog/post_form_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied



#FBV

## 카테고리 모아보기
def categories_page(request, slug):
    if slug=='no-category':
        category='미분류',
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category = category)

    context = {
        'categories': Category.objects.all(),
        'no_category_count': Post.objects.filter(category=None).count(),
        'category': category,
        'post_list': post_list
    }
    return render(
        request,
        'blog/post_list.html',
        context
    )


## 태그 모아보기
def tags_page(request, slug) :
    tag = Tag.objects.get(slug = slug)
    # 태그의 엘레멘트가 포함된 포스트를 모두 찾아야 함
    post_list = tag.post_set.all()

    context = {
        'tag': tag,
        'categories': Category.objects.all(),
        'post_list': post_list,
        'no_category_count' : Post.objects.filter(category=None).count()
    }
    return render(request, 'blog/post_list.html', context)


# 새로운 코멘트 입력
def new_comment(request, pk):
    if request.user.is_authenticated:   # 1. 인증 여부 확인
        post= get_object_or_404(Post, pk=pk)
        if request.method == 'POST':    # 2. 메서드가 POST일 경우
            # request.POST : 사용자가 폼에 입력한 데이터를 담고 있는 POST 요청 객체
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid(): # 3. 폼 유효성 검사 통과시
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())

    else:
        raise PermissionDenied