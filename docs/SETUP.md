# 설치 및 실행 가이드

`django/` 블로그 애플리케이션을 로컬에서 실행하는 방법입니다.

## 요구 사항

- Python 3.10 이상
- pip / venv

## 1. 저장소 클론

```bash
git clone git@github.com:YonggyuCho/django.git cyg-dev
cd cyg-dev
```

## 2. 가상환경 생성 및 활성화

```bash
cd django
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

## 3. 의존성 설치

```bash
pip install -r ../requirements.txt
```

설치되는 주요 패키지:

| 패키지 | 버전 | 용도 |
|--------|------|------|
| Django | 5.2.11 | 웹 프레임워크 |
| pillow | 12.1.1 | 이미지 필드 처리 |
| asgiref | 3.11.1 | ASGI 지원 (Django 의존성) |
| sqlparse | 0.5.5 | SQL 파싱 (Django 의존성) |

## 4. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

> 저장소에는 `db.sqlite3`가 포함되지 않으므로, 최초 실행 시 마이그레이션으로 DB를 새로 생성합니다.

## 5. 관리자 계정 생성 (선택)

```bash
python manage.py createsuperuser
```

생성 후 http://127.0.0.1:8000/admin/ 에서 게시글·태그·댓글을 관리할 수 있습니다.

## 6. 개발 서버 실행

```bash
python manage.py runserver
```

접속 주소:

| 경로 | 설명 |
|------|------|
| `/` | 랜딩 페이지 |
| `/blog/` | 게시글 목록 |
| `/blog/<pk>/` | 게시글 상세 |
| `/about_me/` | 자기소개 |
| `/admin/` | 관리자 |

## 자주 쓰는 관리 명령어

```bash
python manage.py makemigrations   # 모델 변경 → 마이그레이션 파일 생성
python manage.py migrate          # 마이그레이션 DB 반영
python manage.py test             # 테스트 실행
python manage.py shell            # 대화형 셸
python manage.py collectstatic    # 정적 파일 수집 (배포 시)
```

## 환경 설정 주의

`config/settings.py`는 개발 편의를 위해 다음처럼 설정되어 있습니다.

- `DEBUG = True`
- `SECRET_KEY`가 소스에 하드코딩됨
- `ALLOWED_HOSTS`에 `'*'` 포함

**운영 배포 시 반드시 다음을 적용하세요.**

- `DEBUG = False`
- `SECRET_KEY`를 환경변수로 분리
- `ALLOWED_HOSTS`를 실제 도메인으로 제한
- 미디어/정적 파일을 웹서버에서 직접 서빙

## RAG 스크립트 실행

`RAG/test.py`는 `openai` 패키지가 필요합니다(현재 `requirements.txt`에는 미포함).

```bash
pip install openai
python RAG/test.py
```

OpenAI API 키 등 별도 설정이 필요할 수 있습니다.
