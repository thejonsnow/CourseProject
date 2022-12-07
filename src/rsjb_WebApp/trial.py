import json
import requests
import google.oauth2.id_token
import google.auth.transport.requests
import urllib
import os
from flask import Flask, render_template, request

app = Flask(__name__) #creating the Flask class object   
 
@app.route('/') #decorator drfines the   
def home():  
    return render_template('index.html') 

@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form.get('uquery')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./cred.json"

        requesters = google.auth.transport.requests.Request()
        audience = 'https://us-central1-cs410-7733e.cloudfunctions.net/function-1'
        TOKEN = google.oauth2.id_token.fetch_id_token(requesters, audience)

        r = requests.post(
            'https://us-central1-cs410-7733e.cloudfunctions.net/function-1', 
            headers={'Authorization': f"Bearer {TOKEN}", "Content-Type": "application/json"},
            data=json.dumps({"query": form_data})  # possible request parameters
        )
        a = r.content
        b = a.decode()
        c = b.split('{')
        e = {}
        i = 1
        for x in c:
            d = x.split('\n')
            e[i] = d
            i += 1
        del e[1]    
        i = 1    
        result = {}    
        for y,z in e.items():
            f = z
            t = []
            for w in f:
                if "twit" in w:
                    t.append(w)
            result[i] = t
            i += 1
        return render_template('data.html',form_data = result)

app.run(host='localhost', port=5000)

if __name__ =='__main__':  
    app.run(debug = True)  