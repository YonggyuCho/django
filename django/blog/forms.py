from django import forms  # Django 폼 모듈
from .models import Comment  # Comment 모델 import


class CommentForm(forms.ModelForm):  # ModelForm: 모델 기반 자동 폼 생성
    class Meta:
        model = Comment  # Comment 모델을 기반으로 폼 생성
        fields = ['author', 'content']  # 폼에 표시할 필드 (post, created_at은 자동 처리)
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap 스타일 적용
                'placeholder': '이름',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',  # Bootstrap 스타일 적용
                'placeholder': '댓글을 입력하세요',
                'rows': 3,  # 텍스트 영역 높이
            }),
        }
