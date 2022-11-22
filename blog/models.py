from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'

# 모델 만들기 : class (모델명)(models.Model):
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True) # 비어 있어도 오류 안남
    content = models.TextField()

    # 포스트에 이미지 올리기 -> python pip install Pillow
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # %Y = 2022, %y = 22
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True) # 첫 작성 시 자동으로 시간 저장, 불필요시 괄호 안 삭제
    updated_at = models.DateTimeField(auto_now=True) # 수정 시 자동으로 시간 저장, 불필요시 삭제

    # author 필드 추가
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # category 필드 추가 -> admin.py에 category 모델 등록할 것
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # 제목 보여주기 return f'[{해당 포스트의 pk값}]{해당 포스트의 title값}
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author} : {self.created_at}'

    #get_absolute_url 정의
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
        # a.txt -> a txt
        # b.docx -> b docx
        # c.xlsx -> c xlsx
        # a.b.c.txt -> a b c txt

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} : {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
