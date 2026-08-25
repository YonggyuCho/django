# cyg-dev

Django 학습·실습용 저장소입니다. 블로그 웹 애플리케이션(`django/`)과 RAG 실험 코드(`RAG/`)로 구성되어 있습니다.

## 📦 저장소 구성

| 디렉터리 | 설명 |
|----------|------|
| [`django/`](./django) | Django 5.2 기반 블로그 웹 애플리케이션 (블로그 + 태그 + 댓글 + 소개 페이지) |
| [`RAG/`](./RAG) | OpenAI 클라이언트를 이용한 RAG(검색 증강 생성) 실험 스크립트 |
| [`docs/`](./docs) | 프로젝트 문서 (아키텍처 · 설치 · 라우팅) |

## 🧩 Django 블로그 앱 한눈에 보기

- **`blog`** — 게시글(Post), 태그(Tag), 댓글(Comment) 기능. 목록/상세 페이지는 CBV(`ListView`, `DetailView`), 댓글 작성은 FBV로 구현.
- **`single_page`** — 랜딩 페이지, 자기소개(About Me) 정적 페이지.
- **`config`** — 프로젝트 설정 및 최상위 URL 라우팅.

주요 기능:
- 📝 게시글 CRUD 기반 목록/상세 조회
- 🏷️ 태그별 게시글 필터링 (`/blog/tag/<slug>/`)
- 💬 게시글별 댓글 작성
- 🖼️ 대표 이미지·첨부파일 업로드 (media 파일 서빙)
- 🎨 Bootstrap 기반 반응형 UI

## 🚀 빠른 시작

```bash
cd django
python -m venv venv && source venv/bin/activate
pip install -r ../requirements.txt
python manage.py migrate
python manage.py runserver
```

브라우저에서 http://127.0.0.1:8000/ 접속.

> 자세한 설치·실행 방법은 [docs/SETUP.md](./docs/SETUP.md)를 참고하세요.

## 📚 문서

- [아키텍처 설명](./docs/ARCHITECTURE.md) — 앱 구조, 모델 관계, 요청 흐름
- [설치·실행 가이드](./docs/SETUP.md) — 환경 구성 및 관리 명령어
- [URL / 라우팅 명세](./docs/ROUTES.md) — 전체 엔드포인트 표
- [요구사항 기록](./django/Requirement.md) · [TDD 가이드](./django/TDD.md) — 실습 과정에서 작성된 기존 문서

## 🛠️ 기술 스택

- Python 3.10
- Django 5.2.11
- Pillow 12.1 (이미지 처리)
- SQLite (개발용 DB)
- Bootstrap 5

## ⚠️ 참고

- `db.sqlite3`, `django/venv/`, 업로드된 `_media/` 파일은 `.gitignore`로 제외되어 있습니다.
- `config/settings.py`의 `SECRET_KEY`와 `DEBUG=True`는 **개발용 기본값**입니다. 실제 배포 시 반드시 환경변수로 분리하고 `DEBUG=False`로 설정하세요.
