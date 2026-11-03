from django.shortcuts import render, get_object_or_404, redirect

from .models import Article
# from .forms import ArticleForm
# Create your views here.
# def index(request):
#     return HttpResponse("Главная страница новостей")


# def index(request):
#     return render(request, "news/index.html")

def about(request):
    content = {
        "title": "О нас",
        "text": " мы крутой новостной портал ееее лучшие лол кек чики бомбони",
    }
    return render(request, "news/about.html", content)


def article_detail(request, article_id):
    article = get_object_or_404(
        Article,
        id=article_id,
        is_published=True,
    )

    context = {
        "article": article,
    }

    return render(
        request,
        "news/article_detail.html",
        context,
    )






def index(request):
    articles = Article.objects.filter(
        is_published=True
    ).order_by("-created_at")

    context = {
        "articles": articles,
    }

    return render(
        request,
        "news/index.html",
        context,
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
#
# def edit_article(request, article_id):
#     article = get_object_or_404(
#         Article,
#         id=article_id
#     )
#
#     if request.method == "POST":
#         form = ArticleForm(
#             request.POST,
#             request.FILES,
#             instance=article
#         )
#
#         if form.is_valid():
#             article = form.save()
#
#             if article.is_published:
#                 return redirect(
#                     "article_detail",
#                     article_id=article.id
#                 )
#
#             return redirect("home")
#
#     else:
#         form = ArticleForm(instance=article)
#
#     context = {
#         "form": form,
#         "article": article,
#     }
#
#     return render(
#         request,
#         "news/edit_article.html",
#         context
#     )
#
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