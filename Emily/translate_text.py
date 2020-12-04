import os, requests, uuid, json
def translate(text):
    '''
    need to add translator_text_subscription key and translation_text_endpoint in bash file before starting
    Description: translates the given input into the three languages and tries to identifies the source language.
 input: string in any language
 output: translated_data{
                         "detected language":"source language of original input"
                         "en": "text in english"
                         "hi": "text in hindi"
                         "it": "text in italian"
 }
    :param text:
    :return:
    '''

    key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
    if not key_var_name in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
    subscription_key = os.environ[key_var_name]

    endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
    if not endpoint_var_name in os.environ:
        raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
    endpoint = os.environ[endpoint_var_name]

    path = '/translate?api-version=3.0'
    params = '&to=en&to=hi&to=it'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    translated_text = {}
    translated_text['detected language'] = response[0]['detectedLanguage']['language']
    for i in range(4):
        translated_text[response[0]['translations'][i]['to']] = response[0]['translations'][i]['text']

    return translated_text


output = translate(input("Enter text to translate: "))

print(output)