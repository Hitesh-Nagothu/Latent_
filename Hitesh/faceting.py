import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
import urllib.request
import json
from urllib.parse import quote
import numpy as np
import requests
from collections import OrderedDict
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='e1ca7f505feb48f4bc292c175ae313c4')

import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

cols = ['tweet_id', 'name', 'country', 'score', 'full_text', 'lang', 'sentiment', 'influencer_score']
global clicks
clicks = 0


def get_clicks(clicks):
    return clicks + 1


def get_tweets(query):
    query_text = query  # from search bar
    query_text = quote(query_text)
    inurl = 'http://3.84.185.191:8983/solr/gettingstarted/select?defType=dismax&fl=user.name%2Cid%2Cscore' \
            '%2Csentiment_type%2Cinfluencer_score%2Cfull_text%2C%20lang%2C%20country&q=' + query_text + \
            '&qf=full_text&rows=1000 '
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']

    tweets_list = []
    for tweet in docs:

        info = []
        id = tweet['id']
        if 'user.name' in tweet.keys():
            name = tweet['user.name']
        else:
            name = ''
        country = tweet['country'][0]
        score = tweet['score']
        text = tweet['full_text']
        lang = tweet['lang'][0]
        sentiment = tweet['sentiment_type'][0]
        influencer_score = tweet['influencer_score'][0]

        info.append([id, name, country, score, text, lang, sentiment, influencer_score])

        tweets_list.append(info[0])

    tweets_df = pd.DataFrame(data=tweets_list,
                             columns=['tweet_id', 'name', 'country', 'score', 'full_text', 'lang', 'sentiment',
                                      'influencer_score'])
    return tweets_df


# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.layout=html.Div([

    #first block
    html.Div(children=[
                        dcc.Input(id="input1", value="", type="text", placeholder="Enter Query here and click on Submit",
                        style=dict(width='68%'), debounce=True)
    ],style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),

    #second block
    html.Div(children=[
        html.Div(id='container')
    ],style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),

    #3rd block
    html.Div(children=[
        html.Div(id='news')
    ],style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'})

])

@app.callback(
    Output('container', 'children'),
    Input('input1', 'value'),
    State('container', 'children')
)
def display_results(query, children):
    tweets_df = get_tweets(query)

    data = tweets_df.to_dict('rows')

    new_child = html.Div(id={'type': 'one', 'index': 'value'},

                         children=[
                             #dcc.Dropdown(
                              #   id={
                               #      'type': 'dynamic-dropdown',
                                #     'index': 'sentiment'

                                # },
                                 #options=[{'label': s, 'value': s} for s in np.sort(tweets_df['sentiment'].unique())],
                                 #value=['']
                             #),
                             dash_table.DataTable(
                                 id={
                                     'type': 'dynamic-table',
                                     'index': 'results'
                                 },

                                 data=tweets_df.to_dict('rows'),
                                 columns=[{"name": i, "id": i} for i in tweets_df.columns],

                                 style_header={
                                     'backgroundColor': 'DodgerBlue',
                                     'fontWeight': 'bold'
                                 },
                                 hidden_columns=['tweet_id', 'country', 'score', 'lang', 'influencer_score'],

                                 filter_action="native",
                                 sort_action="native",
                                 sort_mode="multi",

                                 page_action="native",
                                 page_current=0,
                                 page_size=10,
                             )
                         ]
                         )

    return new_child


@app.callback(
    Output('news', 'children'),
    Input('input1', 'value')
)
def display_news(value):
    if value is not None:
        all_articles = newsapi.get_everything(q=value,
                                              domains='bbc.co.uk,techcrunch.com',
                                              sort_by='relevancy',
                                              page=2)

        articles = []

        for news in all_articles['articles']:
            info = []
            source = news['source']['name']
            title = news['title']
            url = news['url']

            url_image = news['urlToImage']
            info.append([source, title, url, url_image])
            articles.append(info[0])

        articles_df = pd.DataFrame(articles, columns=['source', 'title', 'url', 'url_image'])

        new_table = html.Div([dash_table.DataTable(
            data=articles_df.to_dict('rows'),
            columns=[{"name": i, "id": i} for i in articles_df.columns],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            hidden_columns=['url_image'],
           )

        ])

        return new_table




"""
@app.callback(
    Output({'type':'dynamic-table','index':'results'}, 'data'),
    Input({'type':'dynamic-dropdown','index':'sentiment'}, 'value'),
    State({'type':'dynamic-table','index':'results'}, 'data')
)
def update_table(value, data):

    tweets = []
    for tweet in data:
        info = []
        info.append(tweet['tweet_id'])
        info.append(tweet['full_text'])
        info.append(tweet['sentiment'])
        tweets.append(info)

    df = pd.DataFrame(tweets, columns=['id', 'full_text','sentiment'])
    sentiment = value[0]
    df = df[df['sentiment'] == sentiment]
    _data = df.to_dict('rows')

    new_table = html.Div([ dash_table.DataTable(
                                 id={
                                     'type': 'dynamic-table',
                                     'index': 'results'
                                 },
                                 data=_data,
                                 columns=[{"name": i, "id": i} for i in cols],
                                 style_data={
                                     'whiteSpace': 'normal',
                                     'height': 'auto'
                                 },
                                 hidden_columns=['tweet_id', 'country', 'score', 'lang', 'influencer_score'],
                                 page_action="native",
                                 page_current=0,
                                 page_size=15)

    ])


    return new_table
"""

if __name__ == '__main__':
    app.run_server(debug=True)
