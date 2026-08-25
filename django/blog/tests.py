from django.test import TestCase, Client  # TestCase: 테스트 기본 클래스, Client: HTTP 요청 시뮬레이션
from django.urls import reverse  # URL 이름으로 실제 URL 경로를 가져오는 함수
from .models import Tag, Post, Comment  # Tag, Post, Comment 모델 import


class PostModelTest(TestCase):
    """Post 모델 테스트 - 모델이 올바르게 생성되고 동작하는지 검증"""

    def setUp(self):
        """각 테스트 실행 전 호출 - 테스트용 데이터 생성"""
        self.post = Post.objects.create(
            title='테스트 제목',
            content='테스트 내용입니다. 이것은 테스트를 위한 게시글입니다.',
        )

    def test_post_creation(self):
        """Post 객체가 정상적으로 생성되는지 테스트"""
        # assertEqual: 두 값이 같은지 비교 (기대값, 실제값)
        self.assertEqual(self.post.title, '테스트 제목')
        self.assertEqual(self.post.content, '테스트 내용입니다. 이것은 테스트를 위한 게시글입니다.')

    def test_post_str(self):
        """Post의 __str__ 메서드가 '[pk] 제목' 형식으로 출력되는지 테스트"""
        expected = f'[{self.post.pk}] 테스트 제목'
        self.assertEqual(str(self.post), expected)

    def test_post_has_created_at(self):
        """Post 생성 시 created_at이 자동으로 설정되는지 테스트"""
        # assertIsNotNone: 값이 None이 아닌지 확인
        self.assertIsNotNone(self.post.created_at)

    def test_post_default_image_blank(self):
        """이미지 없이 생성한 Post의 head_image가 비어있는지 테스트"""
        # blank=True이므로 이미지 없이 생성 가능해야 함
        self.assertFalse(self.post.head_image)

    def test_post_default_file_blank(self):
        """파일 없이 생성한 Post의 file_upload가 비어있는지 테스트"""
        # blank=True이므로 파일 없이 생성 가능해야 함
        self.assertFalse(self.post.file_upload)

    def test_post_title_max_length(self):
        """title 필드의 max_length가 50인지 테스트"""
        max_length = self.post._meta.get_field('title').max_length
        self.assertEqual(max_length, 50)


class PostListViewTest(TestCase):
    """PostList CBV 테스트 - 블로그 목록 페이지 검증"""

    def setUp(self):
        """테스트용 게시글 3개 생성"""
        self.client = Client()  # 테스트용 HTTP 클라이언트
        self.post1 = Post.objects.create(title='첫번째 글', content='내용1')
        self.post2 = Post.objects.create(title='두번째 글', content='내용2')
        self.post3 = Post.objects.create(title='세번째 글', content='내용3')

    def test_post_list_status_code(self):
        """블로그 목록 페이지가 200(정상) 상태코드를 반환하는지 테스트"""
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_uses_correct_template(self):
        """올바른 템플릿(post_list.html)을 사용하는지 테스트"""
        response = self.client.get(reverse('blog:index'))
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_list_contains_posts(self):
        """목록 페이지에 생성한 게시글 제목이 포함되어 있는지 테스트"""
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, '첫번째 글')
        self.assertContains(response, '두번째 글')
        self.assertContains(response, '세번째 글')

    def test_post_list_ordering(self):
        """게시글이 최신순(created_at 내림차순)으로 정렬되는지 테스트"""
        response = self.client.get(reverse('blog:index'))
        posts = response.context['posts']  # 템플릿에 전달된 posts 컨텍스트
        # 첫 번째 항목이 가장 나중에 만든 글이어야 함
        self.assertEqual(posts[0].title, '세번째 글')

    def test_post_list_has_read_more_button(self):
        """목록 페이지에 Read More 버튼이 있는지 테스트"""
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, 'Read More')

    def test_post_list_empty(self):
        """게시글이 없을 때 안내 메시지가 표시되는지 테스트"""
        Post.objects.all().delete()  # 모든 게시글 삭제
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, '아직 포스트가 없습니다.')


class PostDetailViewTest(TestCase):
    """PostDetail CBV 테스트 - 블로그 상세 페이지 검증"""

    def setUp(self):
        """테스트용 게시글 생성"""
        self.client = Client()
        self.post = Post.objects.create(
            title='상세 테스트 글',
            content='이것은 상세 페이지 테스트용 내용입니다.',
        )

    def test_post_detail_status_code(self):
        """상세 페이지가 200(정상) 상태코드를 반환하는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_uses_correct_template(self):
        """올바른 템플릿(post_detail.html)을 사용하는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_detail_contains_title(self):
        """상세 페이지에 게시글 제목이 포함되어 있는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertContains(response, '상세 테스트 글')

    def test_post_detail_contains_content(self):
        """상세 페이지에 게시글 내용이 포함되어 있는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertContains(response, '이것은 상세 페이지 테스트용 내용입니다.')

    def test_post_detail_has_back_button(self):
        """상세 페이지에 목록으로 돌아가기 버튼이 있는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertContains(response, '목록으로 돌아가기')

    def test_post_detail_404_for_invalid_pk(self):
        """존재하지 않는 pk로 접근 시 404를 반환하는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)


class PostImageFileTest(TestCase):
    """이미지/파일 관련 템플릿 조건문 테스트"""

    def setUp(self):
        """이미지 없는 게시글 생성"""
        self.client = Client()
        self.post_no_image = Post.objects.create(
            title='이미지 없는 글',
            content='이미지가 없는 게시글입니다.',
        )

    def test_no_image_no_img_tag(self):
        """이미지가 없는 게시글의 상세 페이지에 <img> 태그가 없는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post_no_image.pk]))
        self.assertNotContains(response, 'card-img-top')

    def test_no_file_no_download_button(self):
        """첨부파일이 없는 게시글에 다운로드 버튼이 없는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post_no_image.pk]))
        self.assertNotContains(response, '첨부파일 다운로드')

    def test_list_no_image_no_img_tag(self):
        """이미지가 없는 게시글의 목록 페이지에 <img> 태그가 없는지 테스트"""
        response = self.client.get(reverse('blog:index'))
        self.assertNotContains(response, 'card-img-top')


class CommentModelTest(TestCase):
    """Comment 모델 테스트 - 댓글이 올바르게 생성되고 동작하는지 검증"""

    def setUp(self):
        """테스트용 Post와 Comment 생성"""
        self.post = Post.objects.create(title='댓글 테스트 글', content='내용')
        self.comment = Comment.objects.create(
            post=self.post,
            author='테스터',
            content='테스트 댓글입니다.',
        )

    def test_comment_creation(self):
        """Comment 객체가 정상적으로 생성되는지 테스트"""
        self.assertEqual(self.comment.author, '테스터')
        self.assertEqual(self.comment.content, '테스트 댓글입니다.')
        self.assertEqual(self.comment.post, self.post)

    def test_comment_str(self):
        """Comment의 __str__ 메서드 출력 형식 테스트"""
        self.assertIn('테스터', str(self.comment))

    def test_comment_related_name(self):
        """Post에서 related_name='comments'로 댓글 접근 가능한지 테스트"""
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(self.post.comments.first(), self.comment)

    def test_comment_cascade_delete(self):
        """Post 삭제 시 댓글도 함께 삭제되는지 테스트 (CASCADE)"""
        self.post.delete()
        self.assertEqual(Comment.objects.count(), 0)


class CommentViewTest(TestCase):
    """댓글 작성 뷰 테스트"""

    def setUp(self):
        self.client = Client()
        self.post = Post.objects.create(title='댓글 뷰 테스트', content='내용')

    def test_add_comment_redirect(self):
        """댓글 작성 후 상세 페이지로 리다이렉트되는지 테스트"""
        response = self.client.post(
            reverse('blog:add_comment', args=[self.post.pk]),
            {'author': '작성자', 'content': '댓글 내용'},
        )
        self.assertEqual(response.status_code, 302)  # 302: 리다이렉트

    def test_add_comment_saves_to_db(self):
        """댓글이 DB에 정상 저장되는지 테스트"""
        self.client.post(
            reverse('blog:add_comment', args=[self.post.pk]),
            {'author': '작성자', 'content': '새 댓글'},
        )
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, '새 댓글')

    def test_comment_displayed_on_detail(self):
        """작성한 댓글이 상세 페이지에 표시되는지 테스트"""
        Comment.objects.create(post=self.post, author='홍길동', content='안녕하세요!')
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertContains(response, '홍길동')
        self.assertContains(response, '안녕하세요!')

    def test_comment_form_on_detail(self):
        """상세 페이지에 댓글 작성 폼이 있는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        self.assertContains(response, '댓글 작성')
        self.assertContains(response, 'csrf')

    def test_add_comment_invalid_pk_404(self):
        """존재하지 않는 Post에 댓글 작성 시 404 반환 테스트"""
        response = self.client.post(
            reverse('blog:add_comment', args=[9999]),
            {'author': '작성자', 'content': '댓글'},
        )
        self.assertEqual(response.status_code, 404)


class TagModelTest(TestCase):
    """Tag 모델 테스트 - 태그가 올바르게 생성되고 동작하는지 검증"""

    def setUp(self):
        """테스트용 Tag 생성"""
        self.tag = Tag.objects.create(name='Python', slug='python')

    def test_tag_creation(self):
        """Tag 객체가 정상적으로 생성되는지 테스트"""
        self.assertEqual(self.tag.name, 'Python')
        self.assertEqual(self.tag.slug, 'python')

    def test_tag_str(self):
        """Tag의 __str__ 메서드가 태그 이름을 출력하는지 테스트"""
        self.assertEqual(str(self.tag), 'Python')

    def test_tag_name_unique(self):
        """Tag name이 unique 제약 조건을 가지는지 테스트"""
        # unique=True이므로 같은 이름의 태그 생성 시 에러 발생
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='Python', slug='python-2')

    def test_tag_slug_unique(self):
        """Tag slug가 unique 제약 조건을 가지는지 테스트"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='Python2', slug='python')

    def test_tag_icon_blank(self):
        """아이콘 없이 Tag 생성이 가능한지 테스트 (blank=True)"""
        self.assertFalse(self.tag.icon)


class TagPostRelationTest(TestCase):
    """Tag-Post 다대다 관계 테스트 - ManyToManyField 동작 검증"""

    def setUp(self):
        """테스트용 Tag와 Post 생성"""
        self.tag_python = Tag.objects.create(name='Python', slug='python')
        self.tag_django = Tag.objects.create(name='Django', slug='django')
        self.post = Post.objects.create(title='테스트 글', content='내용')

    def test_add_tag_to_post(self):
        """Post에 태그를 추가할 수 있는지 테스트"""
        self.post.tags.add(self.tag_python)  # 태그 추가
        self.assertIn(self.tag_python, self.post.tags.all())

    def test_multiple_tags_on_post(self):
        """Post에 여러 태그를 추가할 수 있는지 테스트"""
        self.post.tags.add(self.tag_python, self.tag_django)  # 여러 태그 동시 추가
        self.assertEqual(self.post.tags.count(), 2)

    def test_post_without_tags(self):
        """태그 없이 Post 생성이 가능한지 테스트 (blank=True)"""
        self.assertEqual(self.post.tags.count(), 0)

    def test_tag_reverse_relation(self):
        """Tag에서 Post로 역참조가 가능한지 테스트 (tag.post_set)"""
        self.post.tags.add(self.tag_python)
        # 역참조: Tag에서 해당 태그가 달린 Post 목록 조회
        self.assertIn(self.post, self.tag_python.post_set.all())

    def test_remove_tag_from_post(self):
        """Post에서 태그를 제거할 수 있는지 테스트"""
        self.post.tags.add(self.tag_python)
        self.post.tags.remove(self.tag_python)  # 태그 제거
        self.assertEqual(self.post.tags.count(), 0)


class TagFilterViewTest(TestCase):
    """태그별 필터링 뷰 테스트 - URL로 태그 필터링이 올바르게 동작하는지 검증"""

    def setUp(self):
        """테스트용 Tag, Post 생성 및 태그 연결"""
        self.client = Client()
        self.tag_python = Tag.objects.create(name='Python', slug='python')
        self.tag_django = Tag.objects.create(name='Django', slug='django')
        # Post 2개 생성
        self.post1 = Post.objects.create(title='파이썬 기초', content='내용1')
        self.post2 = Post.objects.create(title='장고 시작', content='내용2')
        # post1에 Python 태그, post2에 Django 태그 연결
        self.post1.tags.add(self.tag_python)
        self.post2.tags.add(self.tag_django)

    def test_tag_filter_status_code(self):
        """태그 필터링 페이지가 200(정상) 상태코드를 반환하는지 테스트"""
        response = self.client.get(reverse('blog:post_list_by_tag', args=['python']))
        self.assertEqual(response.status_code, 200)

    def test_tag_filter_shows_correct_posts(self):
        """태그 필터링 시 해당 태그의 글만 표시되는지 테스트"""
        response = self.client.get(reverse('blog:post_list_by_tag', args=['python']))
        self.assertContains(response, '파이썬 기초')  # Python 태그 글 포함
        self.assertNotContains(response, '장고 시작')  # Django 태그 글 미포함

    def test_tag_filter_shows_current_tag(self):
        """태그 필터링 시 현재 태그명이 페이지에 표시되는지 테스트"""
        response = self.client.get(reverse('blog:post_list_by_tag', args=['python']))
        self.assertContains(response, 'Python')  # 현재 태그명 표시

    def test_tag_filter_shows_all_button(self):
        """태그 필터링 시 '전체 보기' 버튼이 표시되는지 테스트"""
        response = self.client.get(reverse('blog:post_list_by_tag', args=['python']))
        self.assertContains(response, '전체 보기')

    def test_tag_filter_invalid_slug_404(self):
        """존재하지 않는 태그 slug로 접근 시 404를 반환하는지 테스트"""
        response = self.client.get(reverse('blog:post_list_by_tag', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)

    def test_tag_badge_on_post_list(self):
        """목록 페이지에 태그 배지가 표시되는지 테스트"""
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, 'Python')  # 태그 배지 표시

    def test_tag_badge_on_post_detail(self):
        """상세 페이지 제목 옆에 태그 배지가 표시되는지 테스트"""
        response = self.client.get(reverse('blog:post_detail', args=[self.post1.pk]))
        self.assertContains(response, 'Python')  # 제목 옆 태그 배지
