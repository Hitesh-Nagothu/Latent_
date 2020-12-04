from langdetect import detect
from langdetect import DetectorFactory
from googletrans import Translator, constants
from pprint import pprint
import urllib.request
import json
"""
This file is used to translate the query the user entered 
on the website into a url that is passed to Solr.
"""
#---------------------------------------------------------
# The   translate_query   function takes a query and
# translates it into the four following languages: en, hi,
# it, and pt. Returns list with translated query words.
#
# THIS FUNCTION IS NOT WORKING. There is something wrong
# with the imported class googletrans. I left it in here
# in case someone else can get it to work. An explanation
# of what is happening is in the googletrans\gtoken.py file.
#---------------------------------------------------------
"""
def translate_query(query):
    # Will store translated query
    translated_query = []
    
    # init the Google API translator
    translator = Translator()
    
    # Translate query into en, hi, it, and pt and store in translated_query
    translation = translator.translate(str(query), dest='en', src=str(detect(query)))
    translated_query.append(translation)
    translation = translator.translate(str(query), dest='hi', src=str(detect(query)))
    translated_query.append(translation)
    translation = translator.translate(str(query), dest='it', src=str(detect(query)))
    translated_query.append(translation)
    translation = translator.translate(str(query), dest='pt', src=str(detect(query)))
    translated_query.append(translation)
    
    return translated_query
    
"""
#---------------------------------------------------------
# The   solr_url()   function takes a str as an argument
# and creates a url that will be passed to Solr. Returns 
# the created url.
#---------------------------------------------------------
def solr_url(query):
    # Solr url, subject to change based off starting/stopping ec2 instance!
    solr_url = 'http://3.91.150.65:8983/solr/IR2020/'
    # Punctutaion to use in solr_url
    comma = '%2C%20'
    # Use list to search for query in all languages
    langs = ['text_en', 'full_text_en', 'text_hi', 'full_text_hi', 'text_it', 'full_text_it']
    
    # Strip query of [''] format
    query = str(query).strip("['']")

    # This is not working! It is dependent
    # on the translate_query() function working.
    """
    # Translations of query will be stored here
    translated_query = []
    # Translate query into en, hi, it, and pt and store in translated_query list
    translated_query = translate_query(query)
    """
    
    # Create Solr url to search query in all language fields where query is NOT translated.
    #solr_url_with_query = solr_url +'select?fl=' + 'created_at' + comma + 'tweet_lang' + comma + 'country' + comma + 'user.name' + comma + langs[1] + comma + langs[3] + comma  + langs[5] +'&q=' + langs[0] + '%3A%20' + str(query) + '%20OR%20' + langs[2] + '%3A%20' + str(query) + '%20OR%20' + langs[4] + '%3A%20' + str(query) +'&rows=100&wt=json'
    solr_url_with_query = solr_url + 'select?fl=' + 'created_at' + comma + 'tweet_lang' + comma + 'country' + comma + 'user.name' + comma + langs[1] + comma + langs[3] + comma  + langs[5] +'&q=' + '(' + langs[0] + '%3A%20' + '(' + str(query) + ')' + ')' + '%20OR%20' + '(' + langs[2] + '%3A%20' + '(' + str(query) + ')' + ')' + '%20OR%20' + '(' + langs[4] + '%3A%20' + '(' + str(query) + ')' + ')' +'&rows=100&wt=json'
    #solr_url_with_query = 'http://3.91.150.65:8983/solr/IR2020/select?fl=created_at%2C%20tweet_lang%2C%20country%2C%20full_text_en%2C%20full_text_hi%2C%20full_text_it%2C%20%20user.name&q=(text_en%3A%20(mask%20mandate))%20OR%20(text_hi%3A%20(mask%20mandate))%20OR%20(text_it%3A%20(mask%20mandate))&rows=20&wt=json'
    return solr_url_with_query

#---------------------------------------------------------
# The   search_solr()   function takes a url as an
# argument and passes it to Solr. Returns None.
#---------------------------------------------------------
def search_solr(url):
    # Results will be stored in this file in json format
    filename = 'query_results.txt'
    # Open file
    outf = open(filename, 'w', encoding='utf-8')
    
    # Execute url and dump into file
    data = urllib.request.urlopen(url)
    
    docs = json.load(data)['response']['docs']
    # the ranking should start from 1 and increase
    for doc in docs:
        outf.write(str(doc['created_at']) + '\t' + str(doc['tweet_lang']) + '\t' + str(doc['country']) + '\t' + str(doc['user.name']) + '\t' + str(doc['full_text_en']) + '\n')
    
    outf.close()
    
    return filename

#---------------------------------------------------------
# The   main()   function takes the query entered on
# website and calls neccesary functions to return search
# results from Solr. Returns None.
#---------------------------------------------------------    
def main(query):
    # Will store the Solr url returned from function solr_url()
    url = ''
    # Solr results printed here in json format
    results_filename = ''
    # Create Solr url to search Solr with entered query. Store in variable.
    url = solr_url(query)
    # Search Solr and print results to file in json format
    results_filename = search_solr(url)
    
    return results_filename
    