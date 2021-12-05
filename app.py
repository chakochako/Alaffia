import time
from flask.helpers import make_response

import redis
import requests
from flask import Flask,request
import pandas as pd

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
app.config['DEBUG'] = True

def get_request_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

#Call CoinGecko's API to pull the available markets, if not find, return empty list
def coinInquiry(coin):
    markets = []
    res = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin}/tickers')
    if res.status_code == 200:
        resContent = res.json()
        for i in resContent['tickers']: #Iterate all the exchanges and add it to the list to be returned
            markets.append(i.get('market').get('identifier'))
        return markets
    else:
        return markets



@app.route('/', methods = ['POST', 'GET'])
def index():
    count = get_request_count()

    infile = request.get_data() # Read the data from POST
    #infile1 = request.files['file']
    #Convert to Pandas DataFrame based on content_type
    if request.content_type == 'application/json':
        data = pd.read_json(infile)
    elif request.content_type == 'text/csv':
        data = pd.read_csv(infile)
    else:
        pass
    
    db = pd.read_csv('result.csv')

    #Interate all coins from input data
    #Check if it exisits in the current database(result.csv) yet, if not add new records else skip to next coin
    
    for coin in data['id'].tolist():
        m = coinInquiry(coin)
        #teststring = str(m)
        if m:
            if coin in db['id'].tolist(): # if the coin is alrady in the database, update the markets field only
                db.loc[db['id'] == coin, 'exchanges'] = str(m)
            
            else:
                
                #If the coin is not in database, add a new row with current task_run id
                newcoin = pd.DataFrame({'id':coin, 'exchanges':str(m), 'task_run': count},index = [0])
                db = pd.concat([db,newcoin])
                
        else: #If coin code can't be verified by coinGeicko, go to next coin
            continue        
    
    #Export everything back to database(result.csv)
    
    db.to_csv('result.csv', index=False)
    
       
    return 'Processed'
