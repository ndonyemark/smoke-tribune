from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import datetime as dt
from .models import Article, NewsLetterRecipients
from .forms import NewsLetterForm, NewsArticleForm
from .email import send_welcome_email
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MoringaMerch
from .serializer import MerchSerializer

def welcome(request):
    # return HttpResponse("Welcome to the Moringa Tribune")

    return render(request, 'welcome.html')

def news_of_day(request):
    date = dt.date.today()

    return render(request, 'all-news/today-news.html', {'date':date})

def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    form = NewsLetterForm()

    return render(request, 'all-news/today-news.html', {'date': date, 'news': news, 'letterForm': form})

    # if request.method == 'POST':
    #     form = NewsLetterForm(request.POST)
    #     if form.is_valid():
    #         # print('valid')
    #         name = form.cleaned_data['your_name']
    #         email = form.cleaned_data['email']
    #         recipient = NewsLetterRecipients(name = name, email = email)
    #         recipient.save()

    #         print(recipient.name)

    #         send_welcome_email(name, email)

    #         HttpResponseRedirect('news_today')
    
    # else:
    #     form = NewsLetterForm()

    # return render(request, 'all-news/today-news.html', {"date": date, "news": news, 'letterForm': form})

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)
 
def past_days_news(request, past_date):
    try:
        # convert data from the string url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()
    except ValueError:
        # raise 404 error when Value error is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html', {"date": date, "news": news})

def search_results(request):

    if 'article' in request.GET and request.GET['article']:
        search_term = request.GET.get('article')
        searched_articles = Article.search_by_title(search_term)
        message = f'{search_term}'

        return render(request, 'all-news/search.html', {"message": message, "articles": searched_articles})
    
    else:
        message = "you haven't searched for any term"
        return render(request, 'all-news/search.html', message=message)

def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except DoesNotExist:
        raise Http404()

    return render(request, 'all-news/article.html', {'article': article})

@login_required()
def new_article(request):
    current_user = request.user
    print(current_user)
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            print(article.title)
            article.editor = current_user
            article.save()
        return redirect('newsToday')
    
    else:
        form = NewsArticleForm()
    return render(request, 'all-news/news_article.html', {'form': form})

class MerchList(APIView):
    def get(self, request, format=None):
        all_merch = MoringaMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)