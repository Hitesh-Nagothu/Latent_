"""
This file is used to translate the query the user entered 
on the website into a url that is passed to Solr.
"""
#---------------------------------------------------------
# The   solr_url()   function takes a str as an argument
# and creates a url that will be passed to Solr. Returns 
# the created url.
#---------------------------------------------------------
def solr_url(query):
    q = query   # User query is stored in variable q
    start = 0   # Print tweets starting at first tweets
    rows = 20   # Print 20 tweets
    wt = 'csv'  # Print tweets to file in csv format
    filename = "returned_tweets.csv"   #Filename to print tweets in csv format to
    """
        def gallery_items(query):


        solr_tuples = [
            ('q', query),
            ('rows', 20),
            ('start', 0),
            ('fl', 'id, score'),
            ('defType', 'edismax'),
            ('tie','1.0'),
            ('qf', 'text_en text_ru text_de'),
            ('wt', 'json'),

        ]
        if boost_dict[query]=="":
            solr_tuples=solr_tuples[1:]


        return solr_tuples

    for q in queries:
        print(q)
        query_id, query_text = map(str, q.strip().split(" ", 1))
        #query_text = query_text.replace(":", "\:")
        #query_text = quote(query_text)

        solr_tuples = gallery_items(query_text)
        solr_url = 'http://52.207.175.118:8983/solr'
        encoded_solr_tuples = urllib.parse.urlencode(solr_tuples)
        complete_url = solr_url + encoded_solr_tuples

        print(complete_url)

        outf = open(outfn, 'a+')
        data = urllib.request.urlopen(complete_url)
        docs = json.load(data)['response']['docs']

        # the ranking should start from 1 and increase
        rank = 1
        for doc in docs:
            outf.write(
                query_id + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(
                    doc['score']) + ' ' + IRModel + '\n')
            rank += 1
        outf.close()
    """
    url = ''
    return url
    
#---------------------------------------------------------
# The   search_solr()   function takes a url as an
# argument and passes it to Solr. Returns None.
#---------------------------------------------------------
def search_solr():
    
    print("We're in search_solr()")
    return None;