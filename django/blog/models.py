from django.db import models

# Create your models here.

class Tag(models.Model):  # 태그
    name = models.CharField(max_length=50, unique=True)  # 태그 이름 (중복 불가)
    # slug: URL에서 사용할 문자열 (예: "python", "web-dev")
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    # icon: 태그 아이콘 이미지 (선택사항)
    icon = models.ImageField(upload_to='blog/tag_icons/', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model): # 게시물
    title= models.CharField(max_length=50) #제목의 캐릭터 필드 50글자까지
    content = models.TextField() # 게시물의 내용

    # ImageField: 이미지 파일을 업로드/관리하는 필드 (Pillow 라이브러리 필요)
    # upload_to='blog/images/': 업로드된 이미지가 MEDIA_ROOT/blog/images/ 에 저장됨
    # blank=True: 폼에서 빈 값 허용 (이미지 첨부 선택사항)
    head_image = models.ImageField(upload_to='blog/images/', blank=True)

    # FileField: 모든 종류의 파일을 업로드/관리하는 필드
    # upload_to='blog/files/': 업로드된 파일이 MEDIA_ROOT/blog/files/ 에 저장됨
    file_upload = models.FileField(upload_to='blog/files/', blank=True)

    # ManyToManyField: Post와 Tag는 다대다 관계 (글 여러개 ↔ 태그 여러개)
    # blank=True: 태그 없이도 글 작성 가능
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # 날짜
#    author: 작성자는 추후에 DB보고
    updated_at = models.DateTimeField(auto_now_add=True) #업데에트 되는경우에 수정된 시간으로


    def __str__(self):
        return f'[{self.pk}] {self.title}' # DB의 id값 을 출력


class Comment(models.Model):  # 댓글
    # ForeignKey: Post와 1:N 관계 (하나의 Post에 여러 댓글 가능)
    # on_delete=models.CASCADE: Post가 삭제되면 해당 댓글도 함께 삭제
    # related_name='comments': Post에서 post.comments.all()로 댓글 목록 접근 가능
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=30)  # 댓글 작성자 이름
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간 (자동 설정)

    def __str__(self):
        return f'{self.author} - {self.content[:20]}'  # 작성자와 내용 앞 20글자 출력

