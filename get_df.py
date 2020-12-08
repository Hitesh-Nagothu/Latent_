import json
import urllib.request
from urllib.parse import quote


query_text="Joe_Biden"   #from search bar
query_text = quote(query_text)
inurl='http://54.86.70.216:8983/solr/IRP4/select?defType=dismax&fl=id%2Cscore%2Ccountry%2Clang%2Cfull_text&q=JoeBiden&qf=full_text&wt=json'

data = urllib.request.urlopen(inurl)
docs = json.load(data)['response']['docs']
print(docs[0])

tweets_list=[]
for tweet in docs:
      info=[]
      id=tweet['id']
      country=tweet['country'][0]
      score=tweet['score']
      text=tweet['full_text']

      info.append([id,country,score,text])

      tweets_list.append(info[0])

tweets_df = pd.DataFrame(data=tweets_list,
                              columns=['tweet_id','country','score','full_text'])
