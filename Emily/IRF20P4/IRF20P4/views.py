from django.http import HttpResponse
from django.shortcuts import render
from user_queryTOsolr_url import solr_url as su

# Create your views here.
#--- Creates home page view by using home.html.
def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})
    
#--- Creates search page view by using search.html
#    and sends user query to imported function.
def search_view(request, *args, **kwargs):
    users_query = request.POST
    su(users_query.getlist('user_search'))
    return render(request, "search.html", {})

#--- Creates analytics page view by using analytics.html.
def analytics_view(request, *args, **kwargs):
    return render(request, "analytics.html", {})
