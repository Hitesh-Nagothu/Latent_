import json
import urllib.request
from urllib.parse import quote
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash_table
import plotly.graph_objects as go
#from GoogleNews import GoogleNews
from datetime import datetime
from newsapi import NewsApiClient
import plotly.express as px
import time

newsapi = NewsApiClient(api_key='e1ca7f505feb48f4bc292c175ae313c4')
import dash_bootstrap_components as dbc


from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # search bar
    html.Div([
        dbc.Row(
            dbc.Col(
                html.Div([
                             dcc.Input(id="query", type="text", value='', placeholder="Enter Search Here",
                                       debounce=True)] +
                         [html.Div(id='data', children=[], style={'display': 'none'})],
                         style={'display': 'inline-block', 'width': '30%', 'margin-left': '15cm', 'margin-top': '3cm'},

                         ),

            )
        )

    ]),


            dcc.Dropdown(placeholder='Filter By Country', id="country_filter",
                                 options=[{'label': 'USA', 'value': 'USA'},
                                          {'label': 'INDIA', 'value': 'IN'},
                                          {'label': 'ITALY', 'value': 'IT'}],
                                 value=''),

            dcc.Dropdown(placeholder='Filter By POI', id="poi_filter",
                                options=[{'label': 'Narendra Modi', 'value': 'narendramodi'},
                                         {'label': 'Tejaswi Surya', 'value': 'tejaswisurya'},
                                         {'label': 'Zaiapresidente', 'value': 'zaiapresidente'},
                                         {'label': 'Drharshvardhan', 'value': 'drharshvardhan'},
                                         {'label': 'ArvindKejriwal', 'value': 'arvindkejriwal'},
                                         {'label': 'nih', 'value': 'nih'},
                                         {'label': 'luigidimaio', 'value': 'luigidimaio'},
                                         {'label': 'nygovcuomo', 'value': 'nygovcuomo'},
                                         {'label': 'mohfw_india', 'value': 'mohfw_india'},
                                         {'label': 'joebiden', 'value': 'joebiden'},
                                         {'label': 'cdcgov', 'value': 'cdcgov'},
                                         {'label': 'rohanrgupta', 'value': 'rohanrgupta'},
                                         {'label': 'ombirlakota', 'value': 'ombirlakota'},
                                         {'label': 'DonaldTrump', 'value': 'realdonaldtrump'},
                                         {'label': 'giuseppeconteit', 'value': 'giuseppeconteit'},
                                         {'label': 'rashtrapatibhvn', 'value': 'rashtrapatibhvn'},
                                         {'label': 'berluscani', 'value': 'berluscani'}], value=''),



html.Div(
    dbc.Row(
        [
            dbc.Col(html.Div(children=[html.Div(id='table')]), width={"size": 2, "order": "first", "offset": 2},
                    style={'margin-top': '2cm', 'margin-left': '0cm'}),

            dbc.Col(html.Div(children=[html.Div(id='news')]), width=2,
                    style={'margin-top': '2cm'}),
        ],
        justify="center", no_gutters=True,
    ),
),




    html.Div([
        #dcc.Dropdown(id="select_group", options=[{'label': 'All', 'value': 'ALL'},
                                                 #{'label': 'POI', 'value': 'POI'}], value='ALL'),


        html.Div([
            html.Div( [dcc.Markdown("*__LANGUAGE DISTRIBUTION__*"),dcc.Graph(id='language')],
                     style={'width': '33%', 'display': 'inline-block', 'margin-top': '4cm'}),
            html.Div([dcc.Markdown("*__SENTIMENT ANALYSIS__*"),dcc.Graph(id='sentiment')],
                     style={'width': '33%', 'display': 'inline-block', 'margin-top': '4cm'}),
            html.Div([dcc.Markdown("*__COUNTRY-WISE DISTRIBUTION__*"),dcc.Graph(id='country')], style={'width': '33%', 'display': 'inline-block', 'margin-top': '4cm'}),
        ]),


        html.Div([
            html.Div([ dcc.Graph(id='topic_name')],style={'width': '48%', 'display': 'inline-block','margin-top': '4cm'}),
            html.Div([dcc.Graph(id='topic_type')],style={'width': '50%', 'align': 'right', 'display': 'inline-block','margin-top': '4cm'}),
        ]),




        #dcc.Graph(id='topic_name'),
        #dcc.Graph(id='topic_type'),
       # dcc.Graph(id='location')

    ])
])


@app.callback(Output('data', 'children'), Input('query', 'value'))
def create_df(q):
    query_text = q  # from search bar
    query_text = quote(q)

    # inurl='http://34.207.209.38:8983/solr/Topics/select?fl=id%2Cuser.name%2Ccountry%2Cscore%2Cfull_text%2Clang%2Csentiment_type%2Cinfluencer_score&q=*%3A*&wt=json'
    inurl = 'http://34.207.209.38:8983/solr/Topics/select?defType=dismax&fl=user.name%2Cid%2Cscore%2Csentiment_type%2Cinfluencer_score%2Ctopic_type%2Ctopic_name%2Centities.hashtags.text%2Cfull_text%2C%20lang%2C%20country&q=' + query_text + '&qf=full_text&rows=100&wt=json'

    # inurl = 'http://34.207.209.38:8983/solr/Topics/select?fl=id%2Cuser.name%2Ccountry%2Cscore%2Cfull_text%2Clang%2Csentiment_type%2Cinfluencer_score&q=*%3A*'
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
        topic_name = tweet['topic_name'][0]
        topic_type = tweet['topic_type'][0]


        if 'entities.hashtags.text' in tweet.keys():
            hashtags = tweet['entities.hashtags.text']
        else:
            hashtags = ['None']

        sentiment = tweet['sentiment_type']
        influencer_score = tweet['influencer_score'][0]
        #lat=tweet['latitude']
        #lon=tweet['longitude']



        info.append([id, name, country, score, text, lang, sentiment, influencer_score, topic_name, topic_type, hashtags])

        tweets_list.append(info[0])

    tweets_df = pd.DataFrame(data=tweets_list,
                             columns=['tweet_id', 'name', 'country', 'score', 'full_text', 'lang', 'sentiment',
                                      'influencer_score', 'topic_name','topic_type','topic_hashtags'])

    tweets_df = tweets_df.sort_values(by=['influencer_score'])
    tweets_df['sentiment']=tweets_df['sentiment'].apply(lambda row: row[0])

    #tweets_df['latitude'] = pd.to_numeric(tweets_df['latitude'], errors='coerce')
    #tweets_df['longitude'] = pd.to_numeric(tweets_df['longitude'], errors='coerce')

    return tweets_df.to_json()


@app.callback(Output('country_filter', 'value'), [Input('query', 'value')])
def callback(value):
    return ""


@app.callback(Output('poi_filter', 'value'), [Input('query', 'value')])
def callback(value):
    return ""


@app.callback(Output('table', 'children'),
              [Input('data', 'children'), Input('country_filter', 'value'), Input('poi_filter', 'value')])
def display_tweets(data, country_name, poi_name):
    tweets_df = pd.read_json(data, orient='columns')
    ctx = dash.callback_context
    recent = ctx.triggered[0]['prop_id'].split('.')[0]

    if country_name == "" or recent == 'query':
        pass
    else:
        tweets_df = tweets_df[tweets_df['country'] == country_name]

    if poi_name=="":
        pass
    else:
        tweets_df=tweets_df[tweets_df['name']==poi_name]

    new_child = html.Div(id={'type': 'one', 'index': 'value'},

                         children=[

                             dash_table.DataTable(
                                 id={
                                     'type': 'dynamic-table',
                                     'index': 'results'
                                 },

                                 data=tweets_df.to_dict('rows'),
                                 columns=[{"name": i, "id": i} for i in tweets_df.columns],

                                 style_data={
                                     'whiteSpace': 'normal',
                                     'height': 'auto'
                                 },

                                 style_header=
                                 {'backgroundColor': 'rgb(30, 30, 30)'},

                                 style_cell={'textAlign': 'center', 'font-size': '22px', 'font-family': "Calibri",
                                             'maxWidth': 100, 'whiteSpace': 'normal', 'height': 'auto',
                                             'backgroundColor': 'rgb(50, 50, 50)',
                                             'color': 'white',
                                             },
                               

                                 #style_as_list_view=True,

                                 hidden_columns=['tweet_id', 'country', 'score', 'lang', 'influencer_score'],
                                 css=[{"selector": ".show-hide", "rule": "display: none"}],

                                 filter_action="native",
                                 sort_action="native",
                                 sort_mode="multi",
                                 fixed_rows={'headers': True},
                                 style_table={
                                     'overflowy': 'auto',
                                     'overflowx': 'hidden',
                                     'table - layout': 'fixed',

                                     'height': '300px'
                                 },
                                 page_action="none",
                                 # page_current=0
                                 # page_size=20,
                             )
                         ]
                         )

    return new_child


@app.callback(Output('language', 'figure'), Input('data', 'children'))
def plot_language(data):

    tweets_df = pd.read_json(data, orient='columns')
    en_tweets = tweets_df.loc[tweets_df['lang'] == 'en']
    it_tweets = tweets_df.loc[tweets_df['lang'] == 'it']
    hi_tweets = tweets_df.loc[tweets_df['lang'] == 'hi']

    labels = ['English', 'Italian', 'Hindi']
    values = [len(en_tweets), len(it_tweets), len(hi_tweets)]
    colors = ['#003F5C', '#FF6361', '#FFA600', '#7CDDDD']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    return fig


@app.callback(Output('sentiment', 'figure'), Input('data', 'children'))
def plot_sentiment(data):
    tweets_df = pd.read_json(data, orient='columns')

    #tweets_df['sentiment'] = tweets_df['sentiment'].apply(lambda row: str(tweets_df['sentiment'][0]))
    ptweets = tweets_df.loc[tweets_df['sentiment'] == 'Positive']
    ntweets = tweets_df.loc[tweets_df['sentiment'] == 'Negative']
    neutweets = tweets_df.loc[tweets_df['sentiment'] == 'Neutral']

    labels = ['Positive', 'Negative', 'Neutral']
    values = [len(ptweets), len(ntweets), len(neutweets)]
    colors = ['#007ED6', 'red', 'gray']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    return fig


@app.callback(Output('country', 'figure'), Input('data', 'children'))
def plot_country(data):
    tweets_df = pd.read_json(data, orient='columns')

    us_tweets = tweets_df.loc[tweets_df['country'] == 'USA']
    it_tweets = tweets_df.loc[tweets_df['country'] == 'IT']
    hi_tweets = tweets_df.loc[tweets_df['country'] == 'IN']

    labels = ['USA', 'ITALY', 'INDIA']
    values = [len(us_tweets), len(it_tweets), len(hi_tweets)]
    colors = ['#003F5C', '#FF6361', '#FFA600','#7CDDDD']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    return fig


@app.callback(
    Output('news', 'children'),
    Input('query', 'value')
)
def display_news(value):
    time.sleep(1)
    if len(value) > 0:
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

            style_header=
            {'backgroundColor': 'rgb(30, 30, 30)'},

            style_cell={'textAlign': 'center', 'font-size': '22px', 'font-family': "Calibri",
                        'minWidth': 100, 'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                        },
            style_cell_conditional=[
                {'if': {'column_id': 'source'},
                 'width': '10%'},
                {'if': {'column_id': 'title'},
                 'width': '20%'},
                {'if': {'column_id': 'url'},
                 'width': '10%'},
            ],

            style_table={
                'overflowY': 'scroll',
                'height': '200px'
            },
            hidden_columns=['url_image'],
        )

        ])

        return new_table



@app.callback(Output('topic_name', 'figure'), Input('data', 'children'))
def plot_topics(data):
    df = pd.read_json(data, orient='columns')

    df = df.groupby('topic_name').count()
    df = df.sort_values('tweet_id', ascending=False)
    df = df.rename(columns={'tweet_id': 'total_count'})
    df['TOPIC ANALYSIS']=df.index
    fig = px.bar(df, x='TOPIC ANALYSIS', y='total_count')
    fig.layout.plot_bgcolor = 'PINK'
    #fig.layout.paper_bgcolor = 'BLACK'

    return fig

@app.callback(Output('topic_type', 'figure'), Input('data', 'children'))
def plot_topics(data):
    df = pd.read_json(data, orient='columns')
    df = df.groupby('topic_type').count()
    df = df.sort_values('tweet_id', ascending=False)
    df = df.rename(columns={'tweet_id': 'total_count'})
    df['COMPARING COVID AND NON-COVID TWEETS'] = df.index
    fig = px.bar(df, x='COMPARING COVID AND NON-COVID TWEETS', y='total_count')
    fig.layout.plot_bgcolor = 'PINK'

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)

