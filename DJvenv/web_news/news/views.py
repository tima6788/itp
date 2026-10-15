from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
# def index(request):
#     return HttpResponse("Главная страница новостей")


# def index(request):
#     return render(request, "news/index.html")

def index(request):
    context = {
        "title": "Главные новости дня",
        "articles": [
            "В городе открылся новый парк",
            "Учёные представили новую технологию",
            "В университете начался учебный год",
        ],
    }
    return render(request, "news/index.html", context)


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
