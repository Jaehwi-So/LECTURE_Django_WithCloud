import os

from django.contrib.auth.models import User
from django.db import models


#카테고리 : 포스트 = 1 : N
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    # slug : PK대신 읽을 수 있는 텍스트, URL의 일부로 들어가야 하므로(특문제어 등..) 일반 텍스트필드와 다른 SlugField를 사용
    # 관리자페이지에서 이름과 slug값을 똑같이 하려면? -> admin 안에 작성
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)    #unicode 허용으로 한글 허용
    def __str__(self):
        return self.name

    #카테고리의 관리자페이지에서 보여지는 복수형 수정 (Categorys 불편..)
    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    #가로세로 포멧, 저장 위치 등을 지정할 수 있다.
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # 관계 FK (N:1), User가 삭제되면 포스트도 삭제됨
    author = models.ForeignKey(User, on_delete=models.CASCADE)  #파라미터로 함수를 넘겨주는 것(콜백함수), ()를 붙여 실행하지는 않음
#   author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  #Null을 허용, 연관 유저 삭제 시 null로

    # 카테고리 관계 (N : 1), blank=True는 유효성 검사에서 공란허용
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f'[{self.pk}] {self.title} - {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)




