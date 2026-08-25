# TDD (테스트 주도 개발) 가이드

## 테스트 실행 방법

```bash
# 가상환경 활성화
source venv/bin/activate

# 전체 테스트 실행
python manage.py test

# 상세 결과 보기 (--verbosity=2)
python manage.py test --verbosity=2

# 특정 앱만 테스트
python manage.py test blog
python manage.py test single_page

# 특정 테스트 클래스만 실행
python manage.py test blog.tests.PostModelTest
python manage.py test blog.tests.PostListViewTest

# 특정 테스트 메서드 하나만 실행
python manage.py test blog.tests.PostModelTest.test_post_creation
```

---

## 테스트 구조

### blog/tests.py (38개 테스트)

#### 1. PostModelTest — 모델 단위 테스트 (6개)
Post 모델이 올바르게 생성되고 각 필드가 정상 동작하는지 검증

| 테스트 | 설명 | 정상 결과 |
|---|---|---|
| `test_post_creation` | Post 객체 생성 후 title, content 값 확인 | title='테스트 제목', content 일치 |
| `test_post_str` | `__str__` 메서드 출력 형식 확인 | `[1] 테스트 제목` 형식 |
| `test_post_has_created_at` | 생성 시 created_at 자동 설정 확인 | None이 아님 |
| `test_post_default_image_blank` | 이미지 없이 생성 가능한지 확인 | head_image가 비어있음 (blank=True) |
| `test_post_default_file_blank` | 파일 없이 생성 가능한지 확인 | file_upload가 비어있음 (blank=True) |
| `test_post_title_max_length` | title 최대 길이 확인 | max_length=50 |

#### 2. PostListViewTest — 목록 페이지 뷰 테스트 (6개)
PostList(ListView) CBV가 올바르게 동작하는지 검증

| 테스트 | 설명 | 정상 결과 |
|---|---|---|
| `test_post_list_status_code` | /blog/ 접속 시 응답 코드 | 200 OK |
| `test_post_list_uses_correct_template` | 사용 템플릿 확인 | blog/post_list.html |
| `test_post_list_contains_posts` | 게시글 제목들이 페이지에 표시되는지 | 3개 제목 모두 포함 |
| `test_post_list_ordering` | 최신 글이 먼저 나오는지 | 세번째 글이 첫 번째 위치 |
| `test_post_list_has_read_more_button` | Read More 버튼 존재 여부 | 'Read More' 텍스트 포함 |
| `test_post_list_empty` | 게시글 0개일 때 안내 메시지 | '아직 포스트가 없습니다.' 표시 |

#### 3. PostDetailViewTest — 상세 페이지 뷰 테스트 (6개)
PostDetail(DetailView) CBV가 올바르게 동작하는지 검증

| 테스트 | 설명 | 정상 결과 |
|---|---|---|
| `test_post_detail_status_code` | /blog/pk/ 접속 시 응답 코드 | 200 OK |
| `test_post_detail_uses_correct_template` | 사용 템플릿 확인 | blog/post_detail.html |
| `test_post_detail_contains_title` | 게시글 제목 표시 여부 | 제목 포함 |
| `test_post_detail_contains_content` | 게시글 내용 표시 여부 | 내용 포함 |
| `test_post_detail_has_back_button` | 목록으로 돌아가기 버튼 존재 여부 | '목록으로 돌아가기' 텍스트 포함 |
| `test_post_detail_404_for_invalid_pk` | 존재하지 않는 pk 접근 시 | 404 Not Found |

#### 4. PostImageFileTest — 이미지/파일 조건문 테스트 (3개)
템플릿의 {% if %} 조건문이 올바르게 동작하는지 검증

| 테스트 | 설명 | 정상 결과 |
|---|---|---|
| `test_no_image_no_img_tag` | 이미지 없는 글 상세 → img 태그 없음 | 'card-img-top' 미포함 |
| `test_no_file_no_download_button` | 파일 없는 글 → 다운로드 버튼 없음 | '첨부파일 다운로드' 미포함 |
| `test_list_no_image_no_img_tag` | 이미지 없는 글 목록 → img 태그 없음 | 'card-img-top' 미포함 |

#### 7. TagModelTest — Tag 모델 단위 테스트 (5개)
Tag 모델이 올바르게 생성되고 각 필드의 제약 조건이 정상 동작하는지 검증

| 테스트 | 설명 | 정상 결과 |
|---|---|---|
| `test_tag_creation` | Tag 객체 생성 후 name, slug 값 확인 | name='Python', slug='python' |
| `test_tag_str` | `__str__` 메서드가 태그 이름을 출력하는지 확인 | 'Python' |
| `test_tag_name_unique` | 같은 이름의 태그 생성 시 IntegrityError 발생 | 에러 발생 (unique=True) |
| `test_tag_slug_unique` | 같은 slug의 태그 생성 시 IntegrityError 발생 | 에러 발생 (unique=True) |
| `test_tag_icon_blank` | 아이콘 없이 Tag 생성 가능한지 확인 | icon이 비어있음 (blank=True) |

#### 8. TagPostRelationTest — Tag-Post 다대다 관계 테스트 (5개)
ManyToManyField를 통한 Tag-Post 연결이 올바르게 동작하는지 검증

| 테스트 | 설명 | 정상 결과 |
|---|---|---|
| `test_add_tag_to_post` | Post에 태그 추가 가능한지 확인 | tags.all()에 태그 포함 |
| `test_multiple_tags_on_post` | Post에 여러 태그 동시 추가 가능한지 확인 | tags.count() == 2 |
| `test_post_without_tags` | 태그 없이 Post 생성 가능한지 확인 | tags.count() == 0 (blank=True) |
| `test_tag_reverse_relation` | Tag에서 Post로 역참조 가능한지 확인 | tag.post_set.all()에 포함 |
| `test_remove_tag_from_post` | Post에서 태그 제거 가능한지 확인 | tags.count() == 0 |

#### 9. TagFilterViewTest — 태그별 필터링 뷰 테스트 (7개)
태그 slug로 URL 필터링, 태그 배지 표시가 올바르게 동작하는지 검증

| 테스트 | 설명 | 정상 결과 |
|---|---|---|
| `test_tag_filter_status_code` | /blog/tag/python/ 접속 시 응답 코드 | 200 OK |
| `test_tag_filter_shows_correct_posts` | 해당 태그 글만 표시되는지 확인 | Python 글 포함, Django 글 미포함 |
| `test_tag_filter_shows_current_tag` | 현재 태그명이 페이지에 표시되는지 확인 | 'Python' 텍스트 포함 |
| `test_tag_filter_shows_all_button` | '전체 보기' 버튼이 표시되는지 확인 | '전체 보기' 텍스트 포함 |
| `test_tag_filter_invalid_slug_404` | 존재하지 않는 태그 slug 접근 시 | 404 Not Found |
| `test_tag_badge_on_post_list` | 목록 페이지에 태그 배지가 표시되는지 확인 | 'Python' 배지 포함 |
| `test_tag_badge_on_post_detail` | 상세 페이지 제목 옆에 태그 배지 표시 확인 | 'Python' 배지 포함 |

---

### single_page/tests.py (8개 테스트)

#### 5. LandingPageTest — 랜딩 페이지 테스트 (4개)

| 테스트 | 설명 | 정상 결과 |
|---|---|---|
| `test_landing_status_code` | / 접속 시 응답 코드 | 200 OK |
| `test_landing_uses_correct_template` | 사용 템플릿 확인 | single_page/landing.html |
| `test_landing_contains_site_name` | 사이트 이름 표시 여부 | '용규의 웹사이트' 포함 |
| `test_landing_has_blog_link` | 블로그 바로가기 링크 존재 여부 | '블로그 바로가기' 포함 |

#### 6. AboutMePageTest — 자기소개 페이지 테스트 (4개)

| 테스트 | 설명 | 정상 결과 |
|---|---|---|
| `test_about_me_status_code` | /about_me/ 접속 시 응답 코드 | 200 OK |
| `test_about_me_uses_correct_template` | 사용 템플릿 확인 | single_page/about_me.html |
| `test_about_me_contains_name` | 이름 표시 여부 | '조용규' 포함 |
| `test_about_me_contains_company` | 소속 표시 여부 | 'NHN Injeinc' 포함 |

---

## 정상 실행 결과

```
Found 55 test(s).
test_comment_cascade_delete (blog.tests.CommentModelTest) ... ok
test_comment_creation (blog.tests.CommentModelTest) ... ok
test_comment_related_name (blog.tests.CommentModelTest) ... ok
test_comment_str (blog.tests.CommentModelTest) ... ok
test_add_comment_invalid_pk_404 (blog.tests.CommentViewTest) ... ok
test_add_comment_redirect (blog.tests.CommentViewTest) ... ok
test_add_comment_saves_to_db (blog.tests.CommentViewTest) ... ok
test_comment_displayed_on_detail (blog.tests.CommentViewTest) ... ok
test_comment_form_on_detail (blog.tests.CommentViewTest) ... ok
test_post_detail_404_for_invalid_pk (blog.tests.PostDetailViewTest) ... ok
test_post_detail_contains_content (blog.tests.PostDetailViewTest) ... ok
test_post_detail_contains_title (blog.tests.PostDetailViewTest) ... ok
test_post_detail_has_back_button (blog.tests.PostDetailViewTest) ... ok
test_post_detail_status_code (blog.tests.PostDetailViewTest) ... ok
test_post_detail_uses_correct_template (blog.tests.PostDetailViewTest) ... ok
test_list_no_image_no_img_tag (blog.tests.PostImageFileTest) ... ok
test_no_file_no_download_button (blog.tests.PostImageFileTest) ... ok
test_no_image_no_img_tag (blog.tests.PostImageFileTest) ... ok
test_post_list_contains_posts (blog.tests.PostListViewTest) ... ok
test_post_list_empty (blog.tests.PostListViewTest) ... ok
test_post_list_has_read_more_button (blog.tests.PostListViewTest) ... ok
test_post_list_ordering (blog.tests.PostListViewTest) ... ok
test_post_list_status_code (blog.tests.PostListViewTest) ... ok
test_post_list_uses_correct_template (blog.tests.PostListViewTest) ... ok
test_post_creation (blog.tests.PostModelTest) ... ok
test_post_default_file_blank (blog.tests.PostModelTest) ... ok
test_post_default_image_blank (blog.tests.PostModelTest) ... ok
test_post_has_created_at (blog.tests.PostModelTest) ... ok
test_post_str (blog.tests.PostModelTest) ... ok
test_post_title_max_length (blog.tests.PostModelTest) ... ok
test_tag_badge_on_post_detail (blog.tests.TagFilterViewTest) ... ok
test_tag_badge_on_post_list (blog.tests.TagFilterViewTest) ... ok
test_tag_filter_invalid_slug_404 (blog.tests.TagFilterViewTest) ... ok
test_tag_filter_shows_all_button (blog.tests.TagFilterViewTest) ... ok
test_tag_filter_shows_correct_posts (blog.tests.TagFilterViewTest) ... ok
test_tag_filter_shows_current_tag (blog.tests.TagFilterViewTest) ... ok
test_tag_filter_status_code (blog.tests.TagFilterViewTest) ... ok
test_tag_creation (blog.tests.TagModelTest) ... ok
test_tag_icon_blank (blog.tests.TagModelTest) ... ok
test_tag_name_unique (blog.tests.TagModelTest) ... ok
test_tag_slug_unique (blog.tests.TagModelTest) ... ok
test_tag_str (blog.tests.TagModelTest) ... ok
test_add_tag_to_post (blog.tests.TagPostRelationTest) ... ok
test_multiple_tags_on_post (blog.tests.TagPostRelationTest) ... ok
test_post_without_tags (blog.tests.TagPostRelationTest) ... ok
test_remove_tag_from_post (blog.tests.TagPostRelationTest) ... ok
test_tag_reverse_relation (blog.tests.TagPostRelationTest) ... ok
test_about_me_contains_company (single_page.tests.AboutMePageTest) ... ok
test_about_me_contains_name (single_page.tests.AboutMePageTest) ... ok
test_about_me_status_code (single_page.tests.AboutMePageTest) ... ok
test_about_me_uses_correct_template (single_page.tests.AboutMePageTest) ... ok
test_landing_contains_site_name (single_page.tests.LandingPageTest) ... ok
test_landing_has_blog_link (single_page.tests.LandingPageTest) ... ok
test_landing_status_code (single_page.tests.LandingPageTest) ... ok
test_landing_uses_correct_template (single_page.tests.LandingPageTest) ... ok

----------------------------------------------------------------------
Ran 55 tests in 0.178s

OK
```

---

## 주요 테스트 메서드 설명

| 메서드 | 설명 |
|---|---|
| `assertEqual(a, b)` | a와 b가 같은지 확인 |
| `assertIsNotNone(x)` | x가 None이 아닌지 확인 |
| `assertTrue(x)` / `assertFalse(x)` | x가 True/False인지 확인 |
| `assertContains(response, text)` | HTTP 응답에 특정 텍스트가 포함되어 있는지 확인 |
| `assertNotContains(response, text)` | HTTP 응답에 특정 텍스트가 포함되어 있지 않은지 확인 |
| `assertTemplateUsed(response, template)` | 특정 템플릿이 사용되었는지 확인 |

## TDD 사이클

1. **Red** — 실패하는 테스트를 먼저 작성
2. **Green** — 테스트를 통과하는 최소한의 코드 작성
3. **Refactor** — 코드를 정리하고 개선 (테스트는 계속 통과해야 함)

> 새로운 기능을 추가할 때는 반드시 테스트를 먼저 작성하고, 테스트가 통과하도록 코드를 구현합니다.
