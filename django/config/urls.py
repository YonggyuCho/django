"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Django 관리자 모듈
from django.urls import path, include  # URL 라우팅 함수
from django.conf import settings  # Django 설정 가져오기
from django.conf.urls.static import static  # 미디어 파일 URL 서빙 함수

urlpatterns = [
    path('admin/', admin.site.urls),  # /admin/ → Django 관리자 페이지
    path('blog/', include('blog.urls')),  # /blog/ → blog 앱의 URL로 위임
    path('', include('single_page.urls')),  # / → single_page 앱의 URL로 위임
]

# 개발 서버에서 미디어 파일(업로드된 이미지/첨부파일) 서빙
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
