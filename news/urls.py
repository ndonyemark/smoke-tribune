from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
    # url('^$', views.welcome, name='welcome')
    # path('', views.welcome, name='welcome'),
    path('', views.news_today, name='newsToday'),
    re_path('archives/(\d{4}-\d{2}-\d{2})/', views.past_days_news, name='pastNews'),
    path('search/', views.search_results, name='search_results'),
    path('article/<int:article_id>/', views.article, name='article')
]

# if settings.DEBUG:
    # urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 127.0.0.1:8000/news/media/artscle/dog.jpg
