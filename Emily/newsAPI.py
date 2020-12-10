from GoogleNews import GoogleNews
from datetime import datetime
import pandas as pd
#import sys

def retrieve_news(query, created_at, country):
    # Lists of POI names sorted by POI location
    US_POIs = ['Trump', 'Biden', 'Cuomo']
    IN_POIs = ['h1', 'h2', 'h3']
    IT_POIs = ['i1', 'i2', 'i3']
    
    # Dataframe variabled
    USdf = pd.DataFrame()
    INdf = pd.DataFrame()
    ITdf = pd.DataFrame()
        
    # Convert tweet date to Google searchable date
    date = created_at
    converted_datetime = datetime.strftime(datetime.strptime(date,'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
    google_date = str(converted_datetime).split(' ')
    
    # Print results to file. REMOVE FOR WEBSITE vvv
    #original_stdout = sys.stdout
    #with open('GoogleNewsResults.txt', 'w', encoding="utf-8") as f:
        #sys.stdout = f
        
    # Append POI name list to query based off location and search
    if country == 'US':
        for i in US_POIs:
            POI_query = query + ' ' + i
            USresult = search_google_news(POI_query, google_date)
            print(USresult)
    elif country == 'IN':
        for i in IN_POIs:
            POI_query = query + ' ' + i
            INresult = search_google_news(POI_query, google_date)
            print(INresult)
    else:
        for i in IT_POIs:
            POI_query = query + ' ' +i
            ITresult = search_google_news(POI_query, google_date)
            print(ITresult)
        
        #sys.stdout = original_stdout
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    # Can make this return whatever you want for the website, for my testing I put None
    return None

def search_google_news(query, google_date):
    #-- Retrieve news articles
    # Init googlenews
    googlenews = GoogleNews()
    #googlenews.set_period('7d') # Cannot use set_period with set_time_range, use either or.
    #googlenews.set_time_range(str(google_date), '2020-10-12')
    googlenews.set_encode('utf-8')
    googlenews.search(query)
    googlenews.getpage(50)
    result = googlenews.result()
    # Clear before searching again
    googlenews.clear()

    return result
    
"""
Can remove main function once running with website,
main was just used for testing purposes.
"""
if __name__ == '__main__':
    query = 'Trump vaccine'
    created_at = 'Fri Oct 09 10:01:41 +0000 2015'
    country = 'US'
    retrieve_news(query, created_at, country)
