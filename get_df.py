import json
import urllib.request
from urllib.parse import quote
import pandas as pd


query_text="covid"   #from search bar
query_text = quote(query_text)
inurl='http://3.84.185.191:8983/solr/gettingstarted/select?defType=dismax&fl=user.name%2Cid%2Cscore%2Csentiment_type%2Cinfluencer_score%2Cfull_text%2C%20lang%2C%20country&q='+query_text+'&qf=full_text&rows=1000'
data = urllib.request.urlopen(inurl)
docs = json.load(data)['response']['docs']

tweets_list=[]
for tweet in docs:
     
      info=[]
      id=tweet['id']
      if 'user.name' in tweet.keys():
        name=tweet['user.name']
      else:
        name=''
      country=tweet['country'][0]
      score=tweet['score']
      text=tweet['full_text']
      lang=tweet['lang'][0]
      sentiment=tweet['sentiment_type'][0]
      influencer_score=tweet['influencer_score'][0]

      info.append([id,name,country,score,text, lang,sentiment,influencer_score])

      tweets_list.append(info[0])

tweets_df = pd.DataFrame(data=tweets_list,
                              columns=['tweet_id','name','country','score','full_text','lang','sentiment','influencer_score'])
