"""IRF20P4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from pages.views import home_view
from pages.views import search_view
from pages.views import analytics_view
from pages.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('search/', search_view, name='search'),
    path('results/', results_view, name='results'),
    path('analytics/', analytics_view, name='analytics'),
    
    # Sonal's views
    path('', SearchQueryView.as_view(), name='search'),
    path('fetch_tweet_and_replies/', FetchRepliesView.as_view(), name='replies'),
    path('fetch_news/', FetchNewsView.as_view(), name='news'),
    path('fetch_user_news/', FetchUserNewsView.as_view(), name='news'),
    path('fetch_user_tweets/', FetchUserTweetsView.as_view(), name='utweets'),
    
    #misc.
    path('admin/', admin.site.urls),
]
