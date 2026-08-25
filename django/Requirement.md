# 프로젝트 요구사항 기록

## 1. FBV → CBV 변환 (ListView)
- **내용**: `blog/views.py`의 `index` FBV(함수 기반 뷰)를 CBV(클래스 기반 뷰)인 `ListView`로 변환
- **방법**: `from django.views.generic import ListView` 사용, `PostList(ListView)` 클래스 생성
- **설정**: `model = Post`, `ordering = '-created_at'` (최신 글이 위에), `context_object_name = 'posts'`
- **기존 FBV 코드는 주석 처리**, 새 CBV 코드에는 주석으로 설명 추가
- **urls.py**: `views.PostList.as_view()`로 변경, 기존 FBV 라우팅은 주석 처리

## 2. FBV → CBV 변환 (DetailView)
- **내용**: `blog/views.py`의 `post_detail` FBV를 CBV인 `DetailView`로 변환
- **방법**: `from django.views.generic import DetailView` 사용, `PostDetail(DetailView)` 클래스 생성
- **설정**: `model = Post` — DetailView가 자동으로 pk로 조회, 템플릿에 `post`와 `object`로 전달
- **model = Post의 역할 상세 주석 설명** 포함
- **urls.py**: `views.PostDetail.as_view()`로 변경, 기존 FBV 라우팅은 주석 처리

## 3. 템플릿 파일명 Django 기본 규칙으로 변경
- **변경**: `index.html` → `post_list.html` (ListView 기본 규칙: `<앱>/<모델소문자>_list.html`)
- **유지**: `post_detail.html` (DetailView 기본 규칙: `<앱>/<모델소문자>_detail.html`)
- `PostList`에서 `template_name` 제거하여 Django 기본 규칙 자동 적용

## 4. Bootstrap 적용
- **내용**: 모든 템플릿의 직접 작성 CSS를 제거하고 Bootstrap 5.3.3으로 변환
- **적용 대상**: `post_list.html`, `post_detail.html`, `landing.html`, `about_me.html`
- **컴포넌트**: navbar (반응형 햄버거 메뉴 포함), card, btn, list-group 등

## 5. Bootstrap 정적파일 로컬 관리
- **내용**: CDN 대신 `blog/static/blog/bootstrap/`에 Bootstrap CSS/JS 파일을 로컬 저장
- **파일**: `bootstrap.min.css`, `bootstrap.bundle.min.js`
- **템플릿**: `{% load static %}` 태그 로드 후 `{% static 'blog/bootstrap/...' %}`로 참조

## 6. ImageField / FileField 추가
- **내용**: Post 모델에 이미지 업로드(`head_image`)와 파일 업로드(`file_upload`) 필드 추가
- **ImageField**: `upload_to='blog/images/'`, `blank=True` — Pillow 라이브러리 필요
- **FileField**: `upload_to='blog/files/'`, `blank=True`
- **settings.py**: `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / '_media'` 설정
- **config/urls.py**: `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` 추가

## 7. 템플릿 조건문 (if) 처리
- **이미지**: `{% if post.head_image %}` — 이미지가 있는 경우에만 `<img>` 태그 표시
- **첨부파일**: `{% if post.file_upload %}` — 파일이 있는 경우에만 다운로드 버튼 표시
- **다운로드 버튼**: `<a>` 태그에 `download` 속성 추가하여 클릭 시 바로 다운로드

## 8. Read More 버튼 & truncatewords
- **post_list.html**: 본문을 `truncatewords:30`으로 30단어까지만 미리보기 표시
- **Read More 버튼**: `btn btn-success` 스타일로 상세 페이지(`post_detail`)로 이동

## 9. TDD (테스트 주도 개발) 구현
- **내용**: blog 앱과 single_page 앱에 대한 자동화 테스트 작성
- **blog/tests.py**: 모델 테스트(6개), 목록 뷰 테스트(6개), 상세 뷰 테스트(6개), 이미지/파일 조건문 테스트(3개), 댓글 모델 테스트(4개), 댓글 뷰 테스트(5개), 태그 모델 테스트(5개), 태그-Post 관계 테스트(5개), 태그 필터링 뷰 테스트(7개) — 총 47개
- **single_page/tests.py**: 랜딩 페이지 테스트(4개), 자기소개 페이지 테스트(4개) — 총 8개
- **총 55개 테스트**, 모두 통과 (OK)
- **상세 문서**: `TDD.md` 참고 (테스트 실행 방법, 정상 결과, 메서드 설명 포함)

## 10. Post 카드 레이아웃 조정
- **카드 높이 고정**: 모든 Post 카드 동일한 높이(220px), 내용이 길어도 넘치지 않도록 `overflow: hidden`
- **가로 배치**: 왼쪽에 텍스트(제목/작성일/내용/Read More), 오른쪽에 이미지
- **이미지 비율**: 이미지가 카드의 절반 이상 차지 (col-md-7)
- **전체 폭 제한**: `max-width: 780px`로 양옆 여백 확보
- **truncatewords:20**: 카드 크기에 맞게 단어 수 축소

## 11. 템플릿 모듈화 (base.html)
- **내용**: 모든 페이지에 공통으로 사용되는 내비게이션 바와 기본 디자인을 `base.html`로 분리
- **방법**: Django 템플릿 상속 (`{% extends 'base.html' %}`, `{% block %}`) 활용
- **대상**: `post_list.html`, `post_detail.html`, `landing.html`, `about_me.html` 모두 `base.html`을 상속

## 12. 댓글 기능 추가
- **내용**: Post에 댓글을 남길 수 있는 기능 구현
- **Comment 모델**: post(ForeignKey), author(CharField), content(TextField), created_at(DateTimeField)
- **댓글 작성 폼**: post_detail.html 하단에 댓글 입력 폼 표시
- **댓글 목록**: 해당 Post의 댓글을 시간순으로 표시

## 13. 네비게이션 바 / 푸터 모듈화
- **내용**: base.html 내의 navbar와 footer를 별도 파일로 분리하여 모듈화
- **방법**: `{% include %}` 태그로 `navbar.html`, `footer.html`을 base.html에 삽입
- **footer**: 사이트 하단에 저작권 정보 등 공통 푸터 표시

## 14. Tag 기능 추가 (다대다 관계)
- **내용**: Post에 태그를 여러 개 달 수 있는 기능 구현 (ManyToManyField)
- **Tag 모델**: `name`(태그 이름, unique), `slug`(URL용 문자열, allow_unicode), `icon`(ImageField, 선택사항)
- **Post 모델**: `tags = models.ManyToManyField(Tag, blank=True)` 추가
- **태그별 필터링**: `/blog/tag/<slug>/` URL로 해당 태그의 글만 목록 표시
- **post_list.html**: 각 카드에 태그 배지 표시, 클릭 시 해당 태그 글 목록으로 이동
- **post_detail.html**: 제목 옆에 태그 배지 표시, 클릭 시 해당 태그 글 목록으로 이동
- **태그 필터링 시**: 페이지 상단에 현재 태그명(아이콘 포함) + "전체 보기" 버튼 표시
- **아이콘**: Tag에 ImageField로 아이콘 이미지 업로드 가능 (태그명 앞에 표시)
- **Admin**: Tag 모델 admin 사이트에 등록
- **테스트**: TagModelTest(5개), TagPostRelationTest(5개), TagFilterViewTest(7개) — 총 17개 추가
