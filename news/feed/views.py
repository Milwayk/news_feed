from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from feed.forms import CommentForm, NewsForm
from feed.models import Comments, News

def get_base_menu(request):
    menu_items = [
        {"link": "/", "text": "Главная"},
        {"link": "/news/add/", "text": "Опубликовать новость"},
    ]
    if request.user.is_authenticated:
        pass
    else:
        menu_items.extend([
            {"link": "/accounts/registration/", "text": "Регистрация"},
            {"link": "/accounts/login/", "text": "Войти"},
        ])
    return menu_items


def index_page(request):
    context = {
        "page_name": "Страница новостей",
        "menu_items": get_base_menu(request),
        "news_items": News.objects.all(),
    }

    return render(request, "index_page.html", context)


def registration_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    context = {
        "page_name": "Регистрация",
        "menu_items": get_base_menu(request),
    }
    if request.method == "POST":
        registration_form = UserCreationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data.get("username")
            password = registration_form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            context['menu_items'] = get_base_menu(request)
            return redirect("/")
    else:
        registration_form = UserCreationForm()
    context["registration_form"] = registration_form
    return render(request, "registration/registration_page.html", context)



def news_page(request):
    context = {
        "menu_items": get_base_menu(),
        "news_item": News.objects.filter(id=request.GET.get("id"))[0],
    }

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            form.save(news_id=request.GET.get("id"), 
            user=request.user)

    else:
        form = CommentForm()

    context['form'] = form
    context['news_items'] = Comments.objects.filter(news_id=request.GET.get('id'))

    return render(request, "news_page.html", context)


@login_required

def news_add_page(request):
    context = {
        "page_name": "Опубликовать новость",
        "menu_items": get_base_menu(request),
    }

    news_form = NewsForm()
    if request.method == "POST":
        news_form = NewsForm(request.POST)
        if news_form.is_valid():          
            news_form.save(user=request.user)
            return redirect("/")
        
    context['form'] =  news_form
    
    return render(request, "news_add_page.html", context)