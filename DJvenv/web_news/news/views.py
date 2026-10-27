from django.http import HttpResponse
from django.shortcuts import render
from .models import Article

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


def category(request):
    context = {
        "category_name": "Технологии",
        "articles": [
            "Представлена новая модель смартфона",
            "Компания выпустила обновление программного обеспечения",
            "Учёные разработали новый процессор",
        ],
    }
    return render(request, "news/category.html", context)


