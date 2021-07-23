from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import BlogForm
from .models import Blog, Comment
# Create your views here.


def home(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html', {'blogs': blogs})


def detail(request, id):
    blog = Blog.objects.get(id=id)
    return render(request, 'detail.html', {'blog': blog})


def new(request):
    return render(request, 'new.html')


def create(request):
    new_blog = Blog()
    new_blog.title = request.POST['title']
    new_blog.writer = request.POST['writer']
    # 이미지 파일 업로드 안할 시 조건문을 통해 예외처리 해줘야 함
    if request.FILES.get('image') is not None:
        new_blog.image = request.FILES.get('image')
    else:
        pass
    new_blog.body = request.POST['body']
    new_blog.pub_date = timezone.now()
    new_blog.save()
    return redirect('blog:detail', new_blog.id)


def update(request, id):
    blog = Blog.objects.get(id=id)
    if request.method == "POST":
        blog.title = request.POST["title"]
        blog.writer = request.POST["writer"]
        blog.body = request.POST["body"]
        blog.save()
        return redirect('detail', blog.id)
    return render(request, 'update.html', {"blog": blog})


def delete(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect("home")


def new_with_django_form(request):
    form = BlogForm()
    return render(request, 'new_with_django_form.html', {'form': form})


def create_with_django_form(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        new_blog = form.save(commit=False)
        new_blog.pub_date = timezone.now()
        if request.user.is_authenticated:
            new_blog.user = request.user
        new_blog.save()
        return redirect('blog:detail', new_blog.id)
    return redirect('home')


def create_comment(request, id):
    blog = Blog.objects.get(id=id)
    if request.method == "POST":
        new_comment = Comment()
        new_comment.writer = request.POST['writer']
        new_comment.comment = request.POST['comment']
        new_comment.post = blog
        new_comment.save()
        return redirect('blog:detail', blog.id)
    return render(request, 'detail.html', {"blog": blog})
