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
    headers = [
          'twit_id',
          'twit_text',
          'twit_user',
          'twit_user_url',
          'twit_created_at',
          'twit_username',
          'twit_user_avatar_url',
          'twit_user_join_date',
          'twit_user_followers',
          'twit_user_following',
          'twit_user_like_count',
          'twit_user_subscribers_count',
          'twit_user_subscribed_to_count',
          'twit_symbol_title',
          'twit_symbol_symbol',
          'twit_symbol_exchange',
          'twit_symbol_sector',
          'twit_symbol_industry',
          'twit_symbol_logo_url',
          'twit_prices_symbol',
          'twit_prices_price',
          'twit_prices_current_price',
          'twit_prices_change_since_message',
          'twit_prices_percent_change_since_message',
          'twit_likes',
          'twit_entities'
    ]
    data = [headers]
    #change range for more samples if needed
    for i in range(25):
     twit_url = "https://stocktwits.com/user/message/" + str(i)
     page = requests.get(twit_url)
     soup = BeautifulSoup(page.content, 'html.parser')
     twit_text = soup.body.find("script", attrs={"id" : "__NEXT_DATA__"}).string
     twit_json = json.loads(twit_text)
     _d = twit_json['props']['pageProps']['initialData']['message']
     twit_id = _d['id']
     twit_text = _d['body'].replace(',','')
     twit_user = _d['user']['name']
     twit_user_url = "https://stocktwits.com/"+twit_user
     twit_created_at = _d['created_at']

     twit_username = _d['user']['username']
     twit_user_avatar_url = _d['user']['avatar_url']
     twit_user_join_date = _d['user']['join_date']
     twit_user_followers = _d['user']['followers']
     twit_user_following = _d['user']['following']
     twit_user_like_count = _d['user']['like_count']
     twit_user_subscribers_count = _d['user']['subscribers_count']
     twit_user_subscribed_to_count = _d['user']['subscribed_to_count']

     twit_symbol_title = _d['symbol'][0]['title']
     twit_symbol_symbol = _d['symbol'][0]['symbol']
     twit_symbol_exchange = _d['symbol'][0]['exchange']
     twit_symbol_sector = _d['symbol'][0]['sector']
     twit_symbol_industry = _d['symbol'][0]['industry']
     twit_symbol_logo_url = _d['symbol'][0]['logo_url']

     
     twit_prices_symbol = _d['prices'][0]['symbol']
     twit_prices_price = _d['prices'][0]['price']
     twit_prices_current_price = _d['prices'][0]['current_price']
     twit_prices_change_since_message = _d['prices'][0]['change_since_message']
     twit_prices_percent_change_since_message = _d['prices'][0]['percent_change_since_message']
     
     twit_likes = _d['likes']['total']

     twit_entities = _d['entities']['sentiment']['basic']

     data.append([
          twit_id,
          twit_text,
          twit_user,
          twit_user_url,
          twit_created_at,
          twit_username,
          twit_user_avatar_url,
          twit_user_join_date,
          twit_user_followers,
          twit_user_following,
          twit_user_like_count,
          twit_user_subscribers_count,
          twit_user_subscribed_to_count,
          twit_symbol_title,
          twit_symbol_symbol,
          twit_symbol_exchange,
          twit_symbol_sector,
          twit_symbol_industry,
          twit_symbol_logo_url,
          twit_prices_symbol,
          twit_prices_price,
          twit_prices_current_price,
          twit_prices_change_since_message,
          twit_prices_percent_change_since_message,
          twit_likes,
          twit_entities
     ])

    df = pd.DataFrame(data)
    storage_ref = 'example2.csv'
    blob = bucket.blob(storage_ref)
    blob.upload_from_string(df.to_csv())
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
