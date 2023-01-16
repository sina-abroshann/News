from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError

from .forms import ContactForm
from .models import News, Category, Comment, Contact
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from bs4 import BeautifulSoup
import datetime


def home(request):
    first_news = News.objects.last()
    two_news = News.objects.all().order_by('-add_time')[1:3]
    five_categories = Category.objects.all()[0:5]
    return render(request, 'home.html', {
        'first_news': first_news,
        'two_news': two_news,
        'five_categories': five_categories
    })


# All News
def all_news(request):
    all_news = News.objects.all().order_by('-add_time')
    default_page = 1
    page = request.GET.get('page', default_page)
    items_per_page = 5
    paginator = Paginator(all_news, items_per_page)
    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
    return render(request, 'all-news.html', {
        'all_news': all_news,
        'items_page': items_page
    })


# Detail Page
def detail(request, id):
    news = News.objects.get(pk=id)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        comment = request.POST['message']
        try:
            time = request.POST['time']
        except MultiValueDictKeyError:
            time = False
        Comment.objects.create(
            news=news,
            name=name,
            email=email,
            comment=comment,
            time=time
        )
        messages.success(request, 'با تشکر از ثبت دیدگاه')
    category = Category.objects.get(id=news.category.id)
    rel_news = News.objects.filter(category=category).exclude(id=id)
    comments = Comment.objects.filter(news=news, status=True).order_by('-id')
    return render(request, 'detail.html', {
        'news': news,
        'related_news': rel_news,
        'comments': comments
    })


# Fetch all category
def all_category(request):
    cats = Category.objects.all()
    return render(request, 'category.html', {
        'cats': cats
    })


# Fetch all category
def category(request, id):
    category = Category.objects.get(id=id)
    news = News.objects.filter(category=category).order_by('-add_time')
    return render(request, 'category-news.html', {
        'all_news': news,
        'category': category
    })

# scraper
def other(request):
    news_html = requests.get('https://www.yjc.news/fa/rss/allnews')
    news_soup = BeautifulSoup(news_html.content, 'xml')
    items = news_soup.find_all('item')

    title = []
    link = []
    desc = []
    img = []
    date = []

    for item in items:
        title.append(item.title.text)
        link.append(item.link.text)
        desc.append(item.description.text)
        date.append(datetime.datetime.strptime(item.pubDate.text, '%d %b %Y %H:%M:%S +0430'))
        item_img = item.enclosure
        try:
            img.append(item_img.get('url'))
        except:
            img.append('https://dornica.net/uploads/29/nopic.jpg')
    news_scrap = zip(title, link, desc, date, img)
    return render(request, 'other.html', {'news_scrap': news_scrap})

# Contact Us
def ContactView(request):
    if request.method == "POST":
        contact = ContactForm(request.POST or None)
        if contact.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            message = request.POST.get('message')

            contact.name = name
            contact.email = email
            contact.mobile = mobile
            contact.message = message

            contact.save()
            messages.success(request, 'پیام شما با موفقیت ثبت شد.')
            return render(request, 'contact.html', {'form': ContactForm(request.GET)})
        else:
            messages.error(request, 'مشکلی در ثبت پیام شما وجود دارد.')
            messages.error(request, contact.errors)
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
