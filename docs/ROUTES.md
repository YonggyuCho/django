# URL / 라우팅 명세

전체 URL 라우팅은 `config/urls.py`에서 각 앱으로 위임됩니다.

## 최상위 라우팅 (`config/urls.py`)

| Prefix | 위임 대상 | 설명 |
|--------|-----------|------|
| `/admin/` | `admin.site.urls` | Django 관리자 |
| `/blog/` | `blog.urls` | 블로그 앱 |
| `/` | `single_page.urls` | 정적 페이지 앱 |
| `/media/...` | `static()` | 개발 서버 미디어 파일 서빙 |

## 블로그 앱 (`blog/urls.py`, 네임스페이스 `blog`)

| Method | URL | 뷰 | name | 설명 |
|--------|-----|----|------|------|
| GET | `/blog/` | `PostList` | `blog:index` | 전체 게시글 목록 (최신순) |
| GET | `/blog/tag/<slug>/` | `PostList` | `blog:post_list_by_tag` | 특정 태그의 게시글만 필터링 |
| GET | `/blog/<pk>/` | `PostDetail` | `blog:post_detail` | 게시글 상세 + 댓글 폼 |
| POST | `/blog/<pk>/comment/` | `add_comment` | `blog:add_comment` | 댓글 작성 후 상세로 리다이렉트 |

## 정적 페이지 앱 (`single_page/urls.py`, 네임스페이스 `single_page`)

| Method | URL | 뷰 | name | 설명 |
|--------|-----|----|------|------|
| GET | `/` | `landing` | `single_page:landing` | 사이트 랜딩(첫) 페이지 |
| GET | `/about_me/` | `about_me` | `single_page:about_me` | 자기소개 페이지 |

## 템플릿에서의 URL 사용 예

네임스페이스를 사용해 하드코딩 없이 URL을 역참조합니다.

```django
{% url 'blog:index' %}
{% url 'blog:post_detail' pk=post.pk %}
{% url 'blog:post_list_by_tag' slug=tag.slug %}
{% url 'blog:add_comment' pk=post.pk %}
{% url 'single_page:about_me' %}
```

## navbar 활성화 상태

일부 뷰는 `active_nav` 컨텍스트 값을 전달하여 현재 메뉴를 강조합니다.

| 뷰 | `active_nav` 값 |
|----|-----------------|
| `PostList`, `PostDetail` | `'blog'` |
| `about_me` | `'about'` |
