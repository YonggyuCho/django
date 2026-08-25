from django.shortcuts import render  # 템플릿 렌더링 함수


def landing(request):
    """랜딩 페이지 - 사이트 첫 화면"""
    return render(request, 'single_page/landing.html')  # 랜딩 페이지 템플릿 렌더링


def about_me(request):
    """자기소개 페이지"""
    return render(request, 'single_page/about_me.html', {'active_nav': 'about'})  # active_nav로 About Me 메뉴 활성화
