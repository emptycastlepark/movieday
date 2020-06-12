from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.http import JsonResponse

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'community/index.html', context)


def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.save()
            return redirect('community:index')
        else:
            form = ArticleForm()
        context = {
            'form': form
        }
        return render(request, 'community/create.html', context)
    else:
        return redirect('accounts:login')


def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    context = {
        'article': article, 'form': form,
    }
    return render(request, 'community/detail.html', context)


@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.author:
        article.delete()
        return redirect('community:index')
    else:
        return redirect('community:detail', article.pk)


def update(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.author:
            if request.method == 'POST':
                form = ArticleForm(request.POST, instance=article)
                if form.is_valid():
                    article = form.save()
                    return redirect('community:detail', article.pk)
            else:
                form = ArticleForm(instance=article)
            context = {
                'form': form,
                'article': article,
            }
            return render(request, 'community/create.html', context)
        else:
            return redirect('community:detail', article.pk)
    else:
        return redirect('accounts:login')


def like(request, article_pk):
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)
    if article.like_users.filter(pk=user.pk).exists():
        article.like_users.remove(user)
        liked = False
    else:
        article.like_users.add(user)
        liked = True
    return JsonResponse({
        'liked': liked,
        'like_count': article.like_users.count(),
    })


def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
        return redirect('community:detail', article.pk)
    else:
        return redirect('accounts:login')


def comment_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
        return redirect('community:detail', article_pk)
    else:
        return redirect('accounts:login')