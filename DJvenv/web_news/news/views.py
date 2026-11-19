from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleForm
from django.views.decorators.http import require_POST
from .models import Article
# from .forms import ArticleForm
# Create your views here.
# def index(request):
#     return HttpResponse("Главная страница новостей")
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.core.files.storage import default_storage

# def index(request):
#     return render(request, "news/index.html")

def about(request):
    content = {
        "title": "О нас",
        "text": " мы крутой новостной портал ееее лучшие лол кек чики бомбони",
    }
    return render(request, "news/about.html", content)


def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)

    context = {
        "article": article,
    }

    return render(
        request,
        "news/article_detail.html",
        context,
    )


def index(request):

    query = request.GET.get("q", "").strip()

    articles = Article.objects.filter(
        is_published=True,
        is_active=True
    )

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    articles = articles.order_by("-created_at")

    paginator = Paginator(articles, 5)

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    context = {
        "articles": page_obj,
        "page_obj": page_obj,
        "query": query,
    }

    return render(
        request,
        "news/index.html",
        context
    )


def category(request, category_name=None):
    if category_name is None:
        articles = Article.objects.filter(
            is_published=True
        ).order_by("-created_at")

        category_name = "Все категории"
    else:
        articles = Article.objects.filter(
            is_published=True,
            category__iexact=category_name,
        ).order_by("-created_at")

    context = {
        "articles": articles,
        "category_name": category_name,
    }

    return render(
        request,
        "news/category.html",
        context,
    )


@login_required
@permission_required("news.change_article", raise_exception=True)
def edit_article(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            request.FILES,
            instance=article
        )

        if form.is_valid():
            article = form.save()

            if article.is_published:
                return redirect(
                    "article_detail",
                    article_id=article.id
                )

            return redirect("home")

    else:
        form = ArticleForm(instance=article)

    context = {
        "form": form,
        "article": article,
    }

    return render(
        request,
        "news/edit_article.html",
        context
    )


def test_form(request):
    context = {}

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        context = {
            "title": title,
            "content": content,
        }

    return render(
        request,
        "news/test_form.html",
        context,
    )


@login_required
@permission_required("news.add_article", raise_exception=True)
def article_created(request):
    return render(
        request,
        "news/article_created.html",
    )


def add_article(request):
    if request.method == "POST":

        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save()

            return redirect("article_created")


    else:
        form = ArticleForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "news/add_article.html",
        context,
    )


@login_required
@permission_required("news.delete_article", raise_exception=True)
def delete_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id
    )

    if request.method == "POST":

        image_name = article.image.name if article.image else None

        article.delete()

        if image_name:
            image_is_used = Article.objects.filter(
                image=image_name
            ).exists()

            if not image_is_used:
                default_storage.delete(image_name)

        return redirect("home")

    return render(
        request,
        "news/delete_article.html",
        {"article": article}
    )

@login_required
@permission_required("news.change_article", raise_exception=True)
def archive_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        is_active=True
    )

    if request.method == "POST":

        article.is_active = False

        article.save(
            update_fields=["is_active"]
        )

        return redirect("home")

    return render(
        request,
        "news/archive_article.html",
        {"article": article}
    )


@login_required
@permission_required("news.change_article", raise_exception=True)
def restore_article(request, article_id):

    article = get_object_or_404(
        Article,
        id=article_id,
        is_active=False
    )

    if request.method == "POST":

        article.is_active = True

        article.save(
            update_fields=["is_active"]
        )

        return redirect("home")

    return render(
        request,
        "news/restore_article.html",
        {"article": article}
    )

@login_required
@permission_required("news.change_article", raise_exception=True)
def archived_articles(request):

    articles = Article.objects.filter(
        is_active=False
    ).order_by("-created_at")

    return render(
        request,
        "news/archived_articles.html",
        {"articles": articles}
    )