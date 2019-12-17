from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from django.contrib import messages
from .models import Article,Comment

def index(request): 
    return render(request, "index.html")

def about(request): 
    return render(request, "about.html")
    
@login_required(login_url = "user:login")
def dashboard(request): 
    articles = Article.objects.filter(author = request.user)
    
    context = {
        "articles":articles
    }

    return render(request, "dashboard.html", context)

@login_required(login_url = "user:login")
def addArticle(request):    
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():   
        article = form.save(commit = False)
        article.author = request.user
        article.save()

        messages.success(request, "Makaleniz yayınlandı.")
        return redirect("article:dashboard")

    context = {
        "form":form
    }

    return render(request, "addarticle.html", context)

def detail(request, id):
    article = get_object_or_404(Article, id = id)

    comments = article.comments.all()

    context = {
        "article":article,
        "comments":comments
    }

    return render(request, "detail.html", context)

@login_required(login_url = "user:login")
def updateArticle(request, id): 
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)

    if form.is_valid():   
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request, "Makaleniz Güncellendi.")
        return redirect("article:dashboard")

    context = {
        "form":form
    }

    return render(request, "update.html", context)

@login_required(login_url = "user:login")
def deleteArticle(request, id): 
    article = get_object_or_404(Article, id = id)
    if article.author != request.user.username: 
        messages.error(request, "Bu makaleyi silmeye yetkiniz yok veya da böyle bir makale bulunmuyor.")
        return redirect("article:dashboard")
    article.delete()
    messages.success(request, "Makale başarıyla silindi.")
    return redirect("article:dashboard")

def articles(request):  
    keyword = request.GET.get("keyword")

    if keyword: 
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", { "articles":articles })

    articles=Article.objects.all()

    return render(request, "articles.html", { "articles":articles })

def addComment(request, id):    
    article = get_object_or_404(Article, id = id)

    if request.method == "POST": 
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment=Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()

    return redirect(reverse("article:detail", kwargs = { "id":id }))