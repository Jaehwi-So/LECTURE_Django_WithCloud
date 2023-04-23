import os

from django.contrib.auth.models import User
from django.db import models
from markdownx.utils import markdown
from markdownx.models import MarkdownxField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)   #Slug의 한글 허용
    def __str__(self):
        return self.name

    # 테이블 복수명 변경
    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tags/{self.slug}'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    # 이미지업로드 컬럼, 경로는 _media/blog/images/년월일/에 저장
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # 파일업로드 컬럼, ImageField<FileField 상위경로임
    file_upload = models.FileField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # N:1 관계연결, N쪽에만 명시하면 됨
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # N:1 관계연결
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # N:M 관계연결
    tags = models.ManyToManyField(Tag, blank=True)   # null=True를 설정필요없음

    # 오버라이딩 : 대표 객체 속성 설정
    def __str__(self):
        return f'[{self.pk}] - {self.title}'

    # 블로그 상세보기 URL
    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    # 파일 이름
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_content_markdown(self):
        return markdown(self.content)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # (작성자, 포스트) : 댓글 = 1 : N
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} :: {self.content}'

    def get_absolute_url(self):
        # Post View에서 해당 ID 태그의 위치로 이동
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'


class Test(models.Model):
    content = models.TextField()
