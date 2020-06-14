from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def article_index(request):
    articles = Article.objects.all().order_by('-pk')
    # so = request.GET.get('so', 'recent')

    # if so == 'recommend':
    #     articles = Article.objects.annotate(num_like_users=Count('like_users')).order_by('-num_like_users', '-pk')
    # else:
    #     articles = Article.objects.all().order_by('-pk')

    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': articles,
        'page_obj': page_obj
    }
    return render(request, 'community/article_index.html', context)

def article_index_recommend(request):
    articles = Article.objects.annotate(num_like_users=Count('like_users')).order_by('-num_like_users', '-pk')

    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': articles,
        'page_obj': page_obj
    }
    return render(request, 'community/article_index.html', context)


def article_create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.author = request.user
                article.save()
            return redirect('community:article_index')
        else:
            form = ArticleForm()
        context = {
            'form': form
        }
        return render(request, 'community/article_create.html', context)
    else:
        return redirect('accounts:login')


def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    context = {
        'article': article, 'form': form,
    }
    return render(request, 'community/article_detail.html', context)


@require_POST
def article_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.author:
        article.delete()
        return redirect('community:article_index')
    else:
        return redirect('community:article_detail', article.pk)


def article_update(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.author:
            if request.method == 'POST':
                form = ArticleForm(request.POST, instance=article)
                if form.is_valid():
                    article = form.save()
                    return redirect('community:article_detail', article.pk)
            else:
                form = ArticleForm(instance=article)
            context = {
                'form': form,
                'article': article,
            }
            return render(request, 'community/article_create.html', context)
        else:
            return redirect('community:article_detail', article.pk)
    else:
        return redirect('accounts:login')


def article_like(request, article_pk):
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


def article_search(request):
    articles = Article.objects.order_by('-pk')
    kw = request.GET.get('kw', '')
    if kw:
        search_result = articles.filter(
            Q(title__icontains=kw)|
            Q(content__icontains=kw)|
            Q(author__username__icontains=kw)
        ).distinct()

        paginator = Paginator(search_result, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'search_result': search_result,
            'kw': kw,
            'page_obj': page_obj
        }
        return render(request, 'community/article_search.html', context)
    else:
        return redirect('community:article_index')

def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
        return redirect('community:article_detail', article.pk)
    else:
        return redirect('accounts:login')


def comment_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
        return redirect('community:article_detail', article_pk)
    else:
        return redirect('accounts:login')