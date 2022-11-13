from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm
from django.urls import reverse_lazy

# Create your views here.

class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'  #название для шаблона
    #extra_context = {'title':'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):   #переопределяем функцию
        context = super().get_context_data(**kwargs)  #записываем в переменную все что было до этого
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)

class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'  # название для шаблона
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category_id = self.kwargs['category_id'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):   #переопределяем функцию
        context = super().get_context_data(**kwargs)  #записываем в переменную все что было до этого
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    #template_name = 'news/news_detail.html'
    #pk_url_kwarg = 'news_id'

class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    #success_url = reverse_lazy('home')

def index(request):
    news = News.objects.all()
    return render(request, 'news/index.html', {'news': news, 'title': 'Список новостей', })

def test(request):
    return HttpResponse("<h1>test page</h1> ")

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category,})

def view_news (request, news_id):
    #news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {"news_item": news_item})

def add_news (request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            #news = News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})
