import redis
import json
import API_key
import pyEX
import streamlit as st
import IEXstock as IEX
import timedelta

c = pyEX.Client(api_token=API_key.IEX_API_KEY)
r = redis.Redis(host='localhost', port=6379, db=0)


def redis_check(symbol, periods):
# New
    redis_name = f'{symbol}_IS_financials_{periods}Q'
    income_statement = r.get(redis_name)

    if income_statement is None:
        income_statement1 = c.incomeStatement(symbol, period='quarter', last=periods)
        r.set(redis_name, json.dumps(income_statement1))
    else:
       income_statement = json.loads(r.get(redis_name))

    st.write(income_statement)
#

def funVal(symbol,last):

    redis_name = f'{symbol}_FunVal_{last}k'
    funVal = r.get(redis_name)

    if funVal is None:
        funVal = IEX.get_fun(symbol,last)
        r.set(redis_name, json.dumps(funVal))
        #r.expire(redis_name, timedelta(seconds= 5 * 24 * 60 * 60)) # 5 days
    else:
        funVal = json.loads(r.get(redis_name))

    return funVal