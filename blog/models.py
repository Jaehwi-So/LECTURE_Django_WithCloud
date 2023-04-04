import os

from django.contrib.auth.models import User
from django.db import models

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

    def __str__(self):
        return f'[{self.pk}] {self.title} - {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)