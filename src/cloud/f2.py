import base64
import requests
from bs4 import BeautifulSoup
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db, storage
import json
def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    cred = credentials.Certificate('./cred.json')
    app = firebase_admin.initialize_app(cred, {'storageBucket':'cs410-7733e.appspot.com'})
    bucket = storage.bucket(app=app)
    db = firestore.client()
    doc_ref = db.collection(u'twit').document(u'startIndex')
    doc = doc_ref.get()
    start_index = 0
    if doc.exists:
        curr_doc = doc.to_dict()
        start_index = curr_doc['index']
    old_df = pd.read_csv('gs://cs410-7733e.appspot.com/twits1.csv',storage_options={"token": "./cred.json"})
    twit_id = []
    twit_text = []
    twit_user = []
    twit_user_url = []
    twit_created_at = []
    twit_username = []
    twit_user_avatar_url = []
    twit_user_join_date = []
    twit_user_followers = []
    twit_user_following = []
    twit_user_like_count = []
    twit_user_subscribers_count = []
    twit_user_subscribed_to_count = []
    twit_symbol_title = []
    twit_symbol_symbol = []
    twit_symbol_exchange = []
    twit_symbol_sector = []
    twit_symbol_industry = []
    twit_symbol_logo_url = []
    twit_prices_symbol = []
    twit_prices_price = []
    twit_prices_current_price = []
    twit_prices_change_since_message = []
    twit_prices_percent_change_since_message = []
    twit_likes = []
    twit_entities = []
    curr_num = 0
    #change range for more samples if needed
    try:
        for i in range(start_index,start_index+50):
            curr_num = i
            twit_url = "https://stocktwits.com/user/message/" + str(i)
            page = requests.get(twit_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            page.close()
            twit_texts = soup.body.find("script", attrs={"id" : "__NEXT_DATA__"}).string
            twit_json = json.loads(twit_texts)
            _d = twit_json['props']['pageProps']['initialData']['message']
            if _d is not None:
                twit_id.append(_d['id'])
                twit_text.append(_d['body'].replace(',',''))
                twit_user.append(_d['user']['name'])
                twit_username.append(_d['user']['username'])
                twit_user_url.append("https://stocktwits.com/"+_d['user']['username'])
                twit_created_at.append(_d['created_at'])

                twit_user_avatar_url.append(_d['user']['avatar_url'])
                twit_user_join_date.append(_d['user']['join_date'])
                twit_user_followers.append(_d['user']['followers'])
                twit_user_following.append(_d['user']['following'])
                twit_user_like_count.append(_d['user']['like_count'])
                twit_user_subscribers_count.append(_d['user']['subscribers_count'])
                twit_user_subscribed_to_count.append(_d['user']['subscribed_to_count'])

                if 'symbols' in _d and len(_d['symbols']) > 0:
                    twit_symbol_title.append(_d['symbols'][0]['title'])
                    twit_symbol_symbol.append(_d['symbols'][0]['symbol'])
                    twit_symbol_exchange.append(_d['symbols'][0]['exchange'])
                    twit_symbol_sector.append(_d['symbols'][0]['sector'])
                    twit_symbol_industry.append(_d['symbols'][0]['industry'])
                    twit_symbol_logo_url.append(_d['symbols'][0]['logo_url'])
                else:
                    twit_symbol_title.append('null')
                    twit_symbol_symbol.append('null')
                    twit_symbol_exchange.append('null')
                    twit_symbol_sector.append('null')
                    twit_symbol_industry.append('null')
                    twit_symbol_logo_url.append('null')

                if 'prices' in _d and len(_d['prices']) > 0:
                    twit_prices_symbol.append(_d['prices'][0]['symbol'])
                    twit_prices_price.append(_d['prices'][0]['price'])
                    twit_prices_current_price.append(_d['prices'][0]['current_price'])
                    twit_prices_change_since_message.append(_d['prices'][0]['change_since_message'])
                    twit_prices_percent_change_since_message.append(_d['prices'][0]['percent_change_since_message'])
                else:
                    twit_prices_symbol.append('null')
                    twit_prices_price.append('null')
                    twit_prices_current_price.append('null')
                    twit_prices_change_since_message.append('null')
                    twit_prices_percent_change_since_message.append('null')

                if 'likes' in _d and _d['likes'] is not None and 'total' in _d['likes']:
                    twit_likes.append(_d['likes']['total'])
                else:
                    twit_likes.append('null')

                if 'entities' in _d and _d['entities'] is not None and 'sentiment' in _d['entities'] and _d['entities']['sentiment'] is not None and 'basic' in _d['entities']['sentiment']:
                    twit_entities.append(_d['entities']['sentiment']['basic'])
                else:
                    twit_entities.append('null')

            data = {
                'twit_id':twit_id,
                'twit_text':twit_text,
                'twit_user':twit_user,
                'twit_user_url':twit_user_url,
                'twit_created_at':twit_created_at,
                'twit_username':twit_username,
                'twit_user_avatar_url':twit_user_avatar_url,
                'twit_user_join_date':twit_user_join_date,
                'twit_user_followers':twit_user_followers,
                'twit_user_following':twit_user_following,
                'twit_user_like_count':twit_user_like_count,
                'twit_user_subscribers_count':twit_user_subscribers_count,
                'twit_user_subscribed_to_count':twit_user_subscribed_to_count,
                'twit_symbol_title':twit_symbol_title,
                'twit_symbol_symbol':twit_symbol_symbol,
                'twit_symbol_exchange':twit_symbol_exchange,
                'twit_symbol_sector':twit_symbol_sector,
                'twit_symbol_industry':twit_symbol_industry,
                'twit_symbol_logo_url':twit_symbol_logo_url,
                'twit_prices_symbol':twit_prices_symbol,
                'twit_prices_price':twit_prices_price,
                'twit_prices_current_price':twit_prices_current_price,
                'twit_prices_change_since_message':twit_prices_change_since_message,
                'twit_prices_percent_change_since_message':twit_prices_percent_change_since_message,
                'twit_likes':twit_likes,
                'twit_entities':twit_entities
            }
    except:
        #THERE IS DATA OVER WRITING THE GOOD CSV DATA!!!!!!!!!!!!!!!!!!!!!!!
        print('error',curr_num)
        dataIndex = {
            u'index': curr_num,
        }
        doc_ref.set(dataIndex, merge=True)
        df = pd.DataFrame(data)
        storage_ref = 'twits0.csv'
        blob = bucket.blob(storage_ref)
        blob.upload_from_string(df.iloc[0: , :].to_csv())
    dataIndex = {
        u'index': curr_num,
    }
    doc_ref.set(dataIndex, merge=True)
    f1 = pd.DataFrame(data)
    frames = [old_df,f1]
    df = pd.concat(frames)
    storage_ref = 'twits0.csv'
    blob = bucket.blob(storage_ref)
    blob.upload_from_string(df.iloc[0: , :].to_csv())

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
