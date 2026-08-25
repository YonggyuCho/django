from django.shortcuts import render, redirect, get_object_or_404  # 렌더링, 리다이렉트, 404 처리 함수
from django.views.generic import ListView, DetailView  # CBV - 목록 조회용, 상세 조회용 제네릭 뷰
from .models import Tag, Post, Comment  # Tag, Post, Comment 모델 import
from .forms import CommentForm  # 댓글 폼 import


# def index(request):
#     """블로그 메인 페이지 - 모든 포스트 목록"""
#     posts = Post.objects.all().order_by('-created_at')  # 모든 게시글을 최신순으로 조회
#     return render(request, 'blog/index.html', {'posts': posts})  # 템플릿에 posts 데이터 전달


class PostList(ListView):  # CBV 방식으로 블로그 목록 페이지 구현
    model = Post  # Post 모델을 사용
    ordering = '-created_at'  # 최신 게시글이 위에 오도록 정렬
    context_object_name = 'posts'  # 템플릿에서 사용할 변수명 (기본값은 object_list)
    # template_name을 지정하지 않으면 Django가 자동으로 'blog/post_list.html'을 찾음
    # 규칙: <앱이름>/<모델이름소문자>_list.html

    def get_queryset(self):
        """태그 slug가 URL에 있으면 해당 태그의 글만 필터링"""
        queryset = super().get_queryset()  # 기본 queryset (전체 Post, 최신순 정렬)
        tag_slug = self.kwargs.get('slug')  # URL에서 태그 slug 가져오기
        if tag_slug:  # 태그 slug가 있으면
            # tags__slug: ManyToMany 관계를 통해 Tag의 slug 필드로 필터링
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_nav'] = 'blog'  # navbar에서 Blog 메뉴 활성화
        tag_slug = self.kwargs.get('slug')  # URL에서 태그 slug 가져오기
        if tag_slug:  # 태그로 필터링 중이면
            # 현재 선택된 태그 객체를 템플릿에 전달 (제목 옆에 태그 표시용)
            context['current_tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context


# def post_detail(request, pk):
#     """개별 포스트 상세 페이지"""
#     post = Post.objects.get(pk=pk)  # pk(고유번호)에 해당하는 게시글 1개 조회
#     return render(request, 'blog/post_detail.html', {'post': post})  # 템플릿에 post 데이터 전달


class PostDetail(DetailView):  # CBV 방식으로 블로그 상세 페이지 구현
    # model = Post는 이 뷰가 어떤 모델의 데이터를 다룰지 지정하는 것
    # DetailView는 이 설정을 보고 자동으로:
    # 1) URL에서 받은 pk로 Post.objects.get(pk=pk)를 실행하여 해당 게시글을 조회
    # 2) 조회한 객체를 템플릿에 'post'(모델명 소문자)와 'object' 두 가지 이름으로 전달
    # 3) 템플릿 경로를 'blog/post_detail.html' (<앱이름>/<모델이름소문자>_detail.html)로 자동 설정
    model = Post

    def get_context_data(self, **kwargs):
        """템플릿에 댓글 폼을 추가로 전달하기 위해 오버라이드"""
        context = super().get_context_data(**kwargs)  # 기존 컨텍스트(post 등) 가져오기
        context['comment_form'] = CommentForm()  # 빈 댓글 폼을 템플릿에 전달
        context['active_nav'] = 'blog'  # navbar에서 Blog 메뉴 활성화
        return context


def add_comment(request, pk):
    """댓글 작성 FBV - POST 요청으로 댓글을 저장하고 상세 페이지로 리다이렉트"""
    post = get_object_or_404(Post, pk=pk)  # 해당 Post가 없으면 404
    if request.method == 'POST':  # POST 요청일 때만 처리
        form = CommentForm(request.POST)  # 폼에 전송된 데이터 바인딩
        if form.is_valid():  # 유효성 검사 통과 시
            comment = form.save(commit=False)  # DB 저장 전 Comment 객체 생성
            comment.post = post  # 어떤 Post의 댓글인지 연결
            comment.save()  # DB에 저장
    return redirect('blog:post_detail', pk=pk)  # 해당 Post 상세 페이지로 리다이렉트

