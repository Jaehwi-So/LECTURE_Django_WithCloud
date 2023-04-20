from .models import Comment
from django import forms

# 사용할 폼 클래스 생성
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)   #입력
