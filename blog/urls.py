from django.urls import path
from . import views

urlpatterns = [ # IP주소/blog/

  path('', views.PostList.as_view()), # CBV로 포스트 목록 페이지 만들기
  path('<int:pk>/', views.PostDetail.as_view()), # CBV로 포스트 상세 페이지 만들기, single_post_page.html을 post_detail.html로 수정
  path('<int:pk>/new_comment/', views.new_comment),
  path('create_post/', views.PostCreate.as_view()),
  path('update_post/<int:pk>/', views.PostUpdate.as_view()),
  path('category/<str:slug>/', views.category_page)

  #FBV로 포스트 목록 페이지 만들기
  #path('', views.index), # IP주소/blog -> views.py에 index() 함수 정의
  # FBV로 포스트 상세 페이지 만들기
  #path('<int:pk>/', views.single_post_page), line 11
]