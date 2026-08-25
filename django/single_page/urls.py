from django.urls import path  # URL 패턴 정의 함수
from . import views  # 같은 앱의 views 모듈 import

app_name = 'single_page'  # 네임스페이스 설정 (템플릿에서 'single_page:landing' 형태로 사용)

urlpatterns = [
    path('', views.landing, name='landing'),  # / → 랜딩 페이지 (사이트 루트)
    path('about_me/', views.about_me, name='about_me'),  # /about_me/ → 자기소개 페이지
]
