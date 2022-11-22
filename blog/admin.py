from django.contrib import admin
from .models import Post, Category, Comment

# Register your models here.
admin.site.register(Post) #blog 섹션의 post 메뉴 추가 : from .models import post + line 5

# 카테고리 모델 등록
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category,CategoryAdmin)

admin.site.register(Comment)