# 아키텍처

Django 프로젝트 `django/`의 구조와 데이터 모델, 요청 흐름을 정리한 문서입니다.

## 프로젝트 레이아웃

```
django/
├── config/                 # 프로젝트 설정 패키지
│   ├── settings.py         # 설정 (INSTALLED_APPS, DB, 미디어 등)
│   ├── urls.py             # 최상위 URL 라우팅 (admin, blog, single_page)
│   ├── wsgi.py / asgi.py   # 배포용 진입점
├── blog/                   # 블로그 앱 (핵심 기능)
│   ├── models.py           # Post, Tag, Comment 모델
│   ├── views.py            # PostList, PostDetail (CBV), add_comment (FBV)
│   ├── forms.py            # CommentForm (ModelForm)
│   ├── urls.py             # blog 앱 URL 패턴
│   ├── migrations/         # DB 마이그레이션 (0001~0005)
│   ├── templates/blog/     # post_list.html, post_detail.html
│   └── static/blog/        # Bootstrap CSS/JS
├── single_page/            # 정적 페이지 앱
│   ├── views.py            # landing, about_me (FBV)
│   └── templates/single_page/
├── templates/              # 프로젝트 공용 템플릿 (base, navbar, footer)
├── _media/                 # 사용자 업로드 파일 (git 제외)
├── db.sqlite3              # 개발용 DB (git 제외)
└── manage.py
```

## 설치된 앱

`config/settings.py`의 `INSTALLED_APPS`에 사용자 앱 `blog`, `single_page`가 등록되어 있습니다. 나머지는 Django 기본 앱(admin, auth, sessions 등)입니다.

## 데이터 모델

`blog/models.py`에 3개의 모델이 정의되어 있습니다.

### Post (게시글)
| 필드 | 타입 | 설명 |
|------|------|------|
| `title` | CharField(50) | 제목 |
| `content` | TextField | 본문 |
| `head_image` | ImageField | 대표 이미지 (`blog/images/`, 선택) |
| `file_upload` | FileField | 첨부파일 (`blog/files/`, 선택) |
| `tags` | ManyToManyField(Tag) | 태그 (다대다, 선택) |
| `created_at` | DateTimeField | 작성 시각 (자동) |
| `updated_at` | DateTimeField | 수정 시각 (자동) |

### Tag (태그)
| 필드 | 타입 | 설명 |
|------|------|------|
| `name` | CharField(50, unique) | 태그 이름 |
| `slug` | SlugField(unique, allow_unicode) | URL용 슬러그 |
| `icon` | ImageField | 태그 아이콘 (선택) |

### Comment (댓글)
| 필드 | 타입 | 설명 |
|------|------|------|
| `post` | ForeignKey(Post, CASCADE) | 대상 게시글 (`related_name='comments'`) |
| `author` | CharField(30) | 작성자 이름 |
| `content` | TextField | 댓글 내용 |
| `created_at` | DateTimeField | 작성 시각 (자동) |

### 관계 요약

```
Tag  ──< ManyToMany >──  Post  ──< ForeignKey (1:N) >──  Comment
```

- 하나의 Post는 여러 Tag를 가질 수 있고, 하나의 Tag는 여러 Post에 붙을 수 있습니다.
- 하나의 Post는 여러 Comment를 가지며, Post 삭제 시 댓글도 함께 삭제됩니다(CASCADE).

## 뷰 (View) 구성

| 뷰 | 방식 | 역할 |
|----|------|------|
| `PostList` | CBV (`ListView`) | 게시글 목록. `slug`가 있으면 태그로 필터링. 최신순 정렬 |
| `PostDetail` | CBV (`DetailView`) | 게시글 상세. 컨텍스트에 빈 `CommentForm` 추가 |
| `add_comment` | FBV | POST로 댓글 저장 후 상세 페이지로 리다이렉트 |
| `landing` | FBV | 사이트 랜딩 페이지 |
| `about_me` | FBV | 자기소개 페이지 |

> `views.py`에는 FBV(`index`, `post_detail`) 원본이 주석으로 남아 있어 FBV → CBV 전환 과정을 학습용으로 비교할 수 있습니다.

## 요청 흐름 예시

게시글 상세 페이지 요청:

```
GET /blog/3/
  → config/urls.py         (blog/ → blog.urls 위임)
  → blog/urls.py           (<int:pk>/ → PostDetail)
  → PostDetail.get()       (pk=3인 Post 조회)
  → get_context_data()     (post + comment_form 컨텍스트 구성)
  → blog/post_detail.html  (렌더링)
```

댓글 작성 요청:

```
POST /blog/3/comment/
  → add_comment(request, pk=3)
  → CommentForm 유효성 검사 → Comment 저장 (post 연결)
  → redirect blog:post_detail (pk=3)
```

## 템플릿 상속

- `templates/base.html` — 공통 레이아웃 (navbar, footer 포함)
- 각 앱 템플릿은 `base.html`을 상속
- `active_nav` 컨텍스트 값으로 navbar 메뉴 활성화 상태를 표시

## 미디어 파일

- `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / '_media'`
- 개발 서버에서는 `config/urls.py`의 `static()` 헬퍼로 업로드 파일을 서빙합니다.
- 운영 환경에서는 웹서버(Nginx 등)가 미디어를 직접 서빙하도록 별도 설정이 필요합니다.

## RAG 실험 (`RAG/test.py`)

`openai` 클라이언트를 이용한 간단한 문서 검색/임베딩 실험용 스크립트입니다. 사내 규정 문서(`docs`) 리스트를 기반으로 한 RAG 프로토타이핑 초기 단계입니다. Django 앱과는 독립적으로 동작합니다.
