from django.urls import path  # URL 패턴 정의 함수
from . import views  # 같은 앱의 views 모듈 import

app_name = 'blog'  # 네임스페이스 설정 (템플릿에서 'blog:index' 형태로 사용)

urlpatterns = [
    # path('', views.index, name='index'),  # FBV 방식 - 글 목록 페이지
    path('', views.PostList.as_view(), name='index'),  # CBV 방식 - PostList 클래스 뷰로 글 목록 페이지
    path('tag/<str:slug>/', views.PostList.as_view(), name='post_list_by_tag'),  # 태그별 필터링 URL
    # path('<int:pk>/', views.post_detail, name='post_detail'),  # FBV 방식 - 글 상세 페이지
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),  # CBV 방식 - PostDetail 클래스 뷰로 글 상세 페이지
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),  # 댓글 작성 URL (POST 요청)
]
