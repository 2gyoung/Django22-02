from django.shortcuts import render, redirect
from .models import Post, Category, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import postSerializer

class postViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = postSerializer

def delete_comment(request, pk):
    comment = get_object_or_404(Comment,pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url)
    else:
        PermissionDenied

# Create your views here.
# CBV로 포스트 목록 페이지 만들기
class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']
    # 템플릿 post_forms 중복되지 않게 템플릿 이름 지정
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    # 템플릿 post_forms
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self,form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            return super(PostCreate,self).form_valid(form)
        else:
            return redirect('/blog/')

    # 템플릿: 모델평_form.html
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context
class PostList(ListView):
    model = Post
    # blog/templates/blog/index.html의 파일명을 post_list로 수정
    ordering = '-pk' # 포스트 최신순으로 보여주기
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

    # 템플릿 모델명_list.html : post_list.html
    # 파라미터 모델명_list : post_list

# CBV로 포스트 상세 페이지 만들기
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(request, 'blog/post_list.html', {
        'category' : category,
        'post_list' : post_list,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count
    })

    # 템플릿 모델명_detail.html : post_detail.html
    # 파라미터 모델명 : post

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else: #GET
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm
    # CreateView, UpdateView, form을 사용하면
    # 템플릿이 모델명_forms로 생성 : comment_form

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

# FBV로 포스트 목록 페이지 만들 때 필요
#def index(request):
#    posts1 = Post.objects.all().order_by('-pk') -> 최신 등록순으로 보여주기 order_by('-pk')
# 이후 blog/templates/blog에 index.html 생성
#    return render(request, 'blog/index.html', {'posts2': posts1}) -> 포스트 목록 나열
# 이후 index.html에서 {% for p in posts %} <h2><a href="{{ p.get_absolute_url }}">{{ p.title }}</a></h2>
# <h4>{{ p.created_at}}</h4> <p>{{ p.content }}</p> {% endfor %}

# FBV로 포스트 상세 페이지 만들 때 필요
#def single_post_page(request, pk):
#    post3 = Post.objects.get(pk=pk)
#    return render(request, 'blog/single_post_page.html', {'post':post3})
# 이후 blog/templates/blog에 single_post_page.html 생성
# <title>{{ post.title }} - Blog</title>
# <nav><a href="/blog/">Blog</a></nav> <h1>{{ post.title }}</h1> <h4>{{ post.created_at }}</h4> <p>{{ post.content }}</p>