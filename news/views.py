from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
import datetime as dt
from .models import Article

# Create your views here.
def welcome(request):
    return render(request,'welcome.html')


def news_of_day(request):
    date = dt.date.today()
    news = Article.todays_news()

    #Function to convert date object to find exact dates
    # day = convert_dates(date)
    # html = f'''
    #         <html>
    #             <body>
    #                 <h1>News for {day} {date.day}-{date.month}-{date.year}</h1>
    #             </body>
    #         </html>
    #         '''
    return render(request,'all-news/today-news.html',{"date":date,"news":news})

# def convert_dates(dates):
#     ##function that gets the weekday number for dates
#     day_number = dt.date.weekday(dates)

#     days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

#     ##Returning the actual day of the week
#     day = days[day_number]
#     return day

def past_days_news(request,past_date):
    try:
        #Converts data from the string url
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()
    except ValueError:
        #Raise 404 Once value error is thrown
        raise Http404()
        assert False

    # day = convert_dates(date)

    # html = f'''
    #         <html>
    #             <body>
    #                 <h1>News for {day} {date.day}-{date.month}-{date.year}</h1>
    #             </body>
    #         </html>
    #         '''
    news = Article.days_news(date)
    if date == dt.date.today():
        return redirect(news_of_day)
    return render(request,'all-news/past-news.html',{"date":date,"news":news})


def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"
        return render(request,'all-news/search.html',{"message":message,"articles":searched_articles,})
    else:
        message = "You havent searched for any term"
        return render(request,'all-news/search.html',{"messsage":message})

def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html",{"article":article})
