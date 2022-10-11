from django.shortcuts import render
from .models import Post
# Create your views here.
def index(request):
    posts1 = Post.objects.all().order_by('-pk')
    return render(request, 'blog/index.html', {'posts2': posts1})

def single_post_page(request, pk):
    post3 = Post.objects.get(pk=pk)
    return render(request, 'blog/single_post_page.html', {'post':post3})