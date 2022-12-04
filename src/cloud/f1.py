import pandas as pd
import gcsfs
from rank_bm25 import BM25Okapi
import numpy as np
import json

TWIT_PREVIEW_LEN = 40
DEFAULT_TOP_N = 5

class SearchAlgorithm:
    
    def update_ranker(self, corpus, k1=1.5, b=0.75, epsilon=0.25):
        self.corpus = corpus
        tokenized_corpus = [doc.split(" ") for doc in corpus]
        self.ranker = BM25Okapi(tokenized_corpus, k1=k1, b=b, epsilon=epsilon)
        
    def get_scores(self, query):
        tokenized_query = query.split(" ")
        return self.ranker.get_scores(tokenized_query)
    
    def get_top_n(self, query, n=DEFAULT_TOP_N):
        tokenized_query = query.split(" ")
        return self.ranker.get_top_n(tokenized_query, self.corpus, n=n)

def hello_world(request):
    request_json = request.get_json()
    algo = SearchAlgorithm()
    fs = gcsfs.GCSFileSystem(project='cs410-7733e')
    with fs.open('gs://cs410-7733e.appspot.com/example.csv') as f:
        df = pd.read_csv(f)
        print(request_json["query"])
        # if "query" in request_json:
        query = request_json["query"]
        algo.update_ranker(df.twit_text, k1=1.5, b=0.75, epsilon=0.25)
        df["score"] = algo.get_scores(query)
        TOP_N = 3
        search_result = df.sort_values(by=['score'], ascending=False)[:TOP_N]
        array_of_json = json.loads(search_result.to_json(orient="records"))
        indented_str = json.dumps(array_of_json, indent=4)
        return indented_str

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
