
#from django.shortcuts import render
#from django.http import HttpResponse, JsonResponse
#import random
#from .models import Query
#from .serializers import QuerySerializer
#import pdb
#import re
from rest_framework.response import Response
from rest_framework.views import APIView
import urllib.request
from urllib.parse import quote
import json
import os, requests, uuid
from collections import defaultdict
#import pdb
from datetime import datetime
import pandas as pd
#create views here
def index(request):
    return http_response("at search index")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def plot_data(response, highlighting, facet):

    hl_text = ""
    docs = response.get('docs', None)
    total = response['numFound']
    facet_fields = facet['facet_fields']
    sentiment_count = defaultdict(int)
    poi_count = defaultdict(int)
    location_count = defaultdict(int)
    source_count = defaultdict(int)
    hashtag_count = defaultdict(int)
    tweets = []
    time_series = []
    for doc in docs:
        tweet_hash = {}
        doc_id = doc['id']
        hl = highlighting.get(doc_id, {})
        hl_vals = []
        for x in hl.values():
            hl_vals.extend(x)
        if len(hl_vals) > 0:
            hl_text = hl_vals[0]
        else:
            hl_text = doc['full_text']
        tweet_hash['id'] = doc['id']
        tweet_hash['hl_text'] = hl_text
        tweet_hash['sentiment'] = doc['sentiment'][0]
        tweet_hash['user_name'] = doc['user_name'][0]
        tweet_hash['user_screen_name'] = doc['user_screen_name'][0]
        tweet_hash['user_description'] = doc.get('user_description', [None])[0]
        tweet_hash['user_location'] = doc.get('user_location', [None])[0]
        tweet_hash['verified'] = doc['verified'][0]
        tweet_hash['poi_name'] = doc['poi_name'][0]
        tweet_hash['created_at'] = doc['created_at'][0]
        tweet_hash['retweet_count'] = doc['retweet_count'][0]
        tweet_hash['reply_count'] = doc.get('reply_count', 0)
        tweet_hash['article_count'] = doc.get('article_count', 0)
        tweet_hash['profile_url_https'] = doc['user_profile_image_url_https'][0]
        tweet_hash['profile_url'] = doc['user_profile_image_url'][0]
        tweet_hash['in_reply_to_status_id'] = doc.get('in_reply_to_status_id', [None])[0]
        tweet_hash['created_at'] = datetime.strptime(tweet_hash['created_at'][:tweet_hash['created_at'].index('T')],
                                                     '%Y-%m-%d')
        time_series.append([tweet_hash['created_at'], tweet_hash['poi_name']])


        #sentiment analysis
        sentiment_count[doc['sentiment'][0]] +=1
        if 'hashtags' in doc:
            for hashtag in doc['hashtags']:
                hashtag_count[hashtag] +=1

        location_count[doc['sentiment'][0]] +=1
        poi_count[doc['poi_name'][0]] +=1
        #source_count[doc['source'][0]] +=1

        tweets.append(tweet_hash)

        df = pd.DataFrame(time_series, columns=['date', 'name'])
        df = df.groupby(['date', 'name']).size().reset_index(name='count')
        time_series = df.values.tolist()


        #faceted search
        sentiment = {}
        poi = {}
        hashtags = {}
        source = {}
        location = {}
        language = {}
        for key in facet_fields.keys():
            temp = {facet_fields[key][i]: facet_fields[key][i + 1] for i in range(0, len(facet_fields[key]), 2)}
            if key == "hashtags": hashtags = temp
            if key == "sentiment": sentiment = temp
            if key == "poi_name": poi = temp
            if key == "poi_country": location = temp
            if key == "lang": language = temp
            if key == "source": source = temp

        results = {
            'tweets': tweets,
            'analysis': {
                'sentiment': sentiment,
                'poi': poi,
                'location': location,
                'source': source,
                'hashtags': hashtags,
                'language': language,
                'time_series': time_series
            },
            'total': total
        }
        return results

class SearchQueryView(APIView):

    def translate_query(self, text):
     '''need
            to
            add
            translator_text_subscription
            key and translation_text_endpoint in bash
            file
            before
            starting
            Description: translates
            the
            given
            input
            into
            the
            three
            languages and tries
            to
            identifies
            the
            source
            language.

        input: string in any
        language
        output: translated_data
        {
            "detected language": "source language of original input"
                                 "en": "text in english"
                                    "hi": "text in hindi"
                                             "it": "text in italian"
        }
    '''
    #to-do
    #if you want more similar pages

        key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
        subscription_key=

        endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
        endpoint = "https://api.cognitive.microsofttranslator.com/"

        path = '/translate?api-version=3.0'
        params = '&to=en&to=hi&to=it'
        constructed_url = endpoint + path + params

        body = [{
            'text': text
        }]

        #request = requests.post(constructed_url, headers=headers, json=body)
                #response = request.json()
                translated_text = {}
                #translated_text['lang'] = response[0]['detectedLanguage']['language']
                for i in range(4):
                    #translated_text[response[0]['translations'][i]['to']] = response[0]['translations'][i]['text']
                return translated_text

    def process_query(self, query):
        """
        This method processed query and returns the processed query
        :param query:
        :return: query
        """
        # removing new line and escaping all ':'
        query = query.replace("\n", " ")
        query = query.replace(":", "\:")

        # ensuring all words are searched in the given language
        query = "(" + query + ")"
        query = quote(query)

        return query


    def process_filter(self, filter):
        filter_string = ""
        for f in filter:
            filter_string += f + " "
        filter_string = filter_string.strip()

    # removing new line and escaping all ':'
        filter_string = filter_string.replace("\n", " ")
        filter_string = filter_string.replace(":", "\:")

    # ensuring all words are searched in the given language
        filter_string = "(" + filter_string + ")"
        filter_string = quote(filter_string)

        return filter_string

    def get(self, request):
        core_name = "Latent_"
        select_q = "/select?q="
        localhost = "http://18.193.87.200:8983/solr/" + core_name + select_q
        highlight_search = "&hl.fl=full_text,text_*&hl=on&hl.simple.pre=%3Cspan%20class%3D%22tweet-hl%22%3E&" \
                           "hl.simple.post=%3C%2Fspan%3E"
        custom_search = "&defType=edismax&pf=processed_text%5E2&ps=5&hl.fragsize=300" + highlight_search
        fl_score = "&fl=*&wt=json&indent=true"
        query_field = "&qf=full_text%5E0.00001%20"
        stopwords = "&stopwords=true"
        facet_search = "&facet.field=hashtags&facet.field=lang&facet.field=poi_name&facet.field=poi_country&" \
                       "facet.field=sentiment&facet.field=source&facet.sort=count&facet.limit=10&facet=on&facet.mincount=1"

        inurl = ""

        #testing
        #request ={'search': 'family is', 'filters': {'location': ['New York', 'India'], 'poi': ['Trump','Narendra modi'],
        #                                               'hashtags': ['trump','covid']}}


        query = request.GET.get('search', None)
        filters = request.GET.get('qfilters', None)
        #if you want similar tweets like this one
        #analytics=request.GET.get('analytics',False)


        start = request.GET.get('start',0)
        end = request.GET.get('end',20000000)

        limit = "&rows=" +end+ "&start=" +start

        #filters
        hashtags = []
        location = []
        poi = []
        sentiment = []
        source = []
        language = []
        if filters:
            filters = json.loads(filters)
            hashtags = filters.get('hashtags', None)
            location = filters.get('location', None)
            poi = filters.get('poi', None)
            sentiment = filters.get('sentiment', None)
            source = filters.get('source', None)
            language = filters.get('language', None)


            query_hashtag = self.process_filter(hashtags) if hashtags else None
            query_location = self.process_filter(location) if location else None
            query_poi = self.process_filter(poi) if poi else None
            query_sentiment = self.process_filter(sentiment) if sentiment else None
            query_source = self.process_filter(source) if source else None
            query_language = self.process_filter(language) if language else None
            #testing for similar tweets = true so hopefully this should work


    # getting query translated
        translated_query = self.translate_query(query)
        query_en = translated_query['en']
        query_hi = translated_query['hi']
        query_pt = translated_query['pt']
        query_es = translated_query['es']

        # import pdb
        # pdb.set_trace()
        lang_detected = translated_query['lang']
        if lang_detected == "en":
            query_field = query_field + "text_en%5E2%20text_it%5E1%20text_hi%5E1"
        elif lang_detected == "hi":
            query_field = query_field + "text_en%5E1%20text_it%5E1%20text_hi%5E2"
        elif lang_detected == "it":
            query_field = query_field + "text_en%5E1%20text_it%5E1%20text_hi%5E1"


        # processing query
        #ifmoresimilartweets if some similar pages:
            #inurl = localhost +"" + query + highlight_search + facet_search + limit + fl_score
        else
            query = self.process_query(query)
            query_en = self.process_query(query_en)
            query_hi = self.process_query(query_hi)
            query_it = self.process_query(query_it)


            # seperator variable
            or_seperator = "%20OR%20"
            and_seperator = "%20AND%20"

            temp_arr = []
            temp_flag = False

            if hashtags:
                temp_arr.append("hashtags:" + query_hashtag)
                temp_flag = True
            if location:
                temp_arr.append("poi_country:" + query_location)
                temp_flag = True
            if poi:
                temp_arr.append("poi_name:" + query_poi)
                temp_flag = True
            if sentiment:
                temp_arr.append("sentiment:" + query_sentiment)
                temp_flag = True
            if source:
                temp_arr.append("source:" + query_source)
                temp_flag = True
            if language:
                temp_arr.append("lang:" + query_language)
                temp_flag = True

            if temp_flag:
                inurl = localhost + "(" + "processed_text:" + query + or_seperator + "text_en:" + query_en + or_seperator + \
                        "text_hi:" + query_hi + "text_it:" + query_it  + and_seperator + and_seperator.join(temp_arr) + highlight_search + facet_search + limit + fl_score

            elif not inurl:
                inurl = localhost + "processed_text:" + query + or_seperator + "text_en:" + query_en + or_seperator + \
                        "text_hi:" + query_hi + or_seperator + "text_it:" + query_it + or_seperator + custom_search + query_field + facet_search + limit + stopwords + fl_score

        # pdb.set_trace()
        print(inurl)
        data = urllib.request.urlopen(inurl)
        res = json.load(data)
        response = res['response']
        highlighting = res['highlighting']
        facet = res['facet_counts']
        results = plot_data(response, highlighting, facet)
        return Response(results)

class FetchRepliesView(APIView):
    def get(self, request):
        core_name = "Latent_"
        select_q = "/select?q="
        localhost = "http://18.193.87.200:8983/solr/" + core_name + select_q
        facet_search = "&facet.field=hashtags&facet.field=lang&facet.field=poi_name&facet.field=poi_country&" \
                       "facet.field=sentiment&facet.field=source&facet.sort=count&facet.limit=10&facet=on&facet.mincount=1"


        query = request.GET.get('id', None)
        inurl = localhost + 'in_reply_to_status_id:' + query + facet_search + '&rows=20'
        print(inurl)
        data = urllib.request.urlopen(inurl)
        res = json.load(data)
        response = res['response']
        facet = res['facet_counts']
        results = plot_data(response, {}, facet)

        original_tweet_url = localhost + 'id:' + query
        print(original_tweet_url)
        data = urllib.request.urlopen(original_tweet_url)
        res = json.load(data)
        doc = res['response'].get('docs', [None])[0]
        tweet_hash = {}
        doc_id = doc['id']
        hl_text = doc['full_text']
        tweet_hash['id'] = doc['id']
        tweet_hash['hl_text'] = hl_text
        tweet_hash['sentiment'] = doc['sentiment'][0]
        tweet_hash['user_name'] = doc['user_name'][0]
        tweet_hash['user_screen_name'] = doc['user_screen_name'][0]
        tweet_hash['user_description'] = doc.get('user_description', [None])[0]
        tweet_hash['user_location'] = doc.get('user_location', [None])[0]
        tweet_hash['verified'] = doc['verified'][0]
        tweet_hash['poi_name'] = doc['poi_name'][0]
        tweet_hash['created_at'] = doc['created_at'][0]
        tweet_hash['retweet_count'] = doc['retweet_count'][0]
        tweet_hash['reply_count'] = doc.get('reply_count', 0)
        tweet_hash['article_count'] = doc.get('article_count', 0)
        tweet_hash['profile_url_https'] = doc['user_profile_image_url_https'][0]
        tweet_hash['profile_url'] = doc['user_profile_image_url'][0]
        tweet_hash['in_reply_to_status_id'] = doc.get('in_reply_to_status_id', [None])[0]
        results['original_tweet'] = tweet_hash
        return Response(results)

class FetchUserTweetsView(APIView):
    def get(self, request):
        core_name = "Latent_"
        select_q = "/select?q="
        localhost = "http://18.193.87.200:8983/solr/" + core_name + select_q
        facet_search = "&facet.field=hashtags&facet.field=lang&facet.field=poi_name&facet.field=poi_country&" \
                       "facet.field=sentiment&facet.field=source&facet.sort=count&facet.limit=10&facet=on&facet.mincount=1"


        and_seperator = "%20AND%20"
        query = request.GET.get('poi_name', None)
        inurl = localhost + 'poi_name:' + query + and_seperator + 'verified:true' + facet_search + '&rows=20'
        print(inurl)
        data = urllib.request.urlopen(inurl)
        res = json.load(data)
        response = res['response']
        facet = res['facet_counts']
        results = plot_data(response, {}, facet)

        return Response(results)

class FetchNewsView(APIView):
    def get(self, request):
        core_name = "NewsArticles"
        select_q = "/select?q="
        localhost = "http://18.193.87.200:8983/solr/" + core_name + select_q
        query = request.GET.get('id', None)
        inurl = localhost + 'tweet_id:' + query

        data = urllib.request.urlopen(inurl)
        res = json.load(data)
        response = res['response']
        docs = response.get('docs', [None])
        total = response.get('numFound')
        tweets = []
        for doc in docs:
            tweet_hash = dict()
            tweet_hash['tweet_id'] = doc.get('tweet_id')[0]
            tweet_hash['poi_name'] = doc.get('poi_name')
            tweet_hash['source'] = doc.get('name', [None])[0]
            tweet_hash['author'] = doc.get('author', [None])[0]
            tweet_hash['title'] = doc.get('title')[0]
            tweet_hash['description'] = doc.get('description')[0]
            tweet_hash['url'] = doc.get('url')[0]
            tweet_hash['url_to_image'] = doc.get('url_to_image', ['None'])[0]
            tweet_hash['published_date'] = doc.get('published_date')[0]
            tweet_hash['content'] = doc.get('content')[0]
            tweets.append(tweet_hash)

        return Response(tweets)

class FetchUserNewsView(APIView):
    def get(self, request):
        core_name = "NewsArticles"
        select_q = "/select?q="
        localhost = "http://18.193.87.200:8983/solr/" + core_name + select_q
        query = request.GET.get('poi_name', None)
        inurl = localhost + 'poi_name:' + query

        print(inurl)
        data = urllib.request.urlopen(inurl)
        res = json.load(data)
        response = res['response']
        docs = response.get('docs', [None])
        total = response.get('numFound')
        tweets = []
        for doc in docs:
            tweet_hash = dict()
            tweet_hash['tweet_id'] = doc.get('tweet_id')[0]
            tweet_hash['poi_name'] = doc.get('poi_name')
            tweet_hash['source'] = doc.get('name', [None])[0]
            tweet_hash['author'] = doc.get('author', [None])[0]
            tweet_hash['title'] = doc.get('title', [None])[0]
            tweet_hash['description'] = doc.get('description', [None])[0]
            tweet_hash['url'] = doc.get('url', [None])[0]
            tweet_hash['url_to_image'] = doc.get('url_to_image', [None])[0]
            tweet_hash['published_date'] = doc.get('published_date', [None])[0]
            tweet_hash['content'] = doc.get('content', [None])[0]
            tweets.append(tweet_hash)

        return Response(tweets)
