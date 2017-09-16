# Open your GateCoin account via https://gatecoin.com/register?referralCode=CESJBP

import time 
import hmac
import hashlib
import base64
import json
import os.path
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from urllib.request import Request, urlopen

default_encoding = "UTF-8"

load_dotenv(find_dotenv())
api_public_key = os.environ['gatecoin_api_public_key'].encode(default_encoding)
api_private_key = os.environ['gatecoin_api_private_key'].encode(default_encoding)

def balance_get():
    
    requestType = "GET"
    contentType = ""
    url = "https://api.gatecoin.com/Balance/Balances"
    current_time = str(time.time())

    message = (requestType + contentType + url + current_time).lower().encode(default_encoding)

    dig = hmac.new(api_private_key, msg=message, digestmod=hashlib.sha256).digest()
    api_request_signature = base64.b64encode(dig).decode()

    req = Request(url)
    req.add_header("api_public_key", api_public_key)
    req.add_header("api_request_date", current_time)
    req.add_header("api_request_signature", api_request_signature)
    resource = urlopen(req)
    response = resource.read().decode(resource.headers.get_content_charset() or default_encoding)

    balances = json.loads(response)

    def convert_ccy(amt, ccy_from, ccy_to, indirect):
        if(ccy_from == ccy_to or amt == 0):
            return amt

        try:
            url = "https://api.gatecoin.com/Public/LiveTicker/" + ((ccy_to + ccy_from) if indirect else (ccy_from + ccy_to))
            req = Request(url) 
            resource = urlopen(req)
            response = resource.read().decode(resource.headers.get_content_charset() or default_encoding)
            tick = json.loads(response)
            return amt * (1 / tick["ticker"]["last"] if indirect else tick["ticker"]["last"])
        except:
            return 0

    coin_arr = [(b["currency"], b["isDigital"], b["balance"]) for b in balances["balances"]]
    coin_df = pd.DataFrame(coin_arr, columns=["ccy", "is_digital", "in_base"])
    coin_df["in_btc"] = pd.Series(coin_df.apply(lambda row: convert_ccy(row["in_base"], row["ccy"], "BTC", not row["is_digital"]), axis=1))
    coin_df["in_hkd"] = pd.Series(coin_df.apply(lambda row: convert_ccy(row["in_btc"], "BTC", "HKD", False), axis=1))

    return coin_df.to_dict('records')