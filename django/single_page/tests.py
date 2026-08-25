from django.test import TestCase, Client  # TestCase: 테스트 기본 클래스, Client: HTTP 요청 시뮬레이션
from django.urls import reverse  # URL 이름으로 실제 URL 경로를 가져오는 함수


class LandingPageTest(TestCase):
    """랜딩 페이지 테스트"""

    def setUp(self):
        self.client = Client()

    def test_landing_status_code(self):
        """랜딩 페이지가 200(정상) 상태코드를 반환하는지 테스트"""
        response = self.client.get(reverse('single_page:landing'))
        self.assertEqual(response.status_code, 200)

    def test_landing_uses_correct_template(self):
        """올바른 템플릿(landing.html)을 사용하는지 테스트"""
        response = self.client.get(reverse('single_page:landing'))
        self.assertTemplateUsed(response, 'single_page/landing.html')

    def test_landing_contains_site_name(self):
        """랜딩 페이지에 사이트 이름이 포함되어 있는지 테스트"""
        response = self.client.get(reverse('single_page:landing'))
        self.assertContains(response, '용규의 웹사이트')

    def test_landing_has_blog_link(self):
        """랜딩 페이지에 블로그 바로가기 링크가 있는지 테스트"""
        response = self.client.get(reverse('single_page:landing'))
        self.assertContains(response, '블로그 바로가기')


class AboutMePageTest(TestCase):
    """자기소개 페이지 테스트"""

    def setUp(self):
        self.client = Client()

    def test_about_me_status_code(self):
        """자기소개 페이지가 200(정상) 상태코드를 반환하는지 테스트"""
        response = self.client.get(reverse('single_page:about_me'))
        self.assertEqual(response.status_code, 200)

    def test_about_me_uses_correct_template(self):
        """올바른 템플릿(about_me.html)을 사용하는지 테스트"""
        response = self.client.get(reverse('single_page:about_me'))
        self.assertTemplateUsed(response, 'single_page/about_me.html')

    def test_about_me_contains_name(self):
        """자기소개 페이지에 이름이 포함되어 있는지 테스트"""
        response = self.client.get(reverse('single_page:about_me'))
        self.assertContains(response, '조용규')

    def test_about_me_contains_company(self):
        """자기소개 페이지에 소속 정보가 포함되어 있는지 테스트"""
        response = self.client.get(reverse('single_page:about_me'))
        self.assertContains(response, 'NHN Injeinc')
