import mplsoccer as PyPizza
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import API_key
import pyEX
from IEXstock import IEXstock
import IEXstock as IEX
from scipy import stats
import math
import requests

c = pyEX.Client(api_token=API_key.IEX_API_KEY)


def pizza(symbol):
    stock = IEXstock(API_key.IEX_API_KEY, symbol)
    df = pd.DataFrame(c.financials(symbol))
    df = df.rename(index={0: symbol})

    peers = stock.get_peers()

    for x in range(0, len(peers)):
        df1 = pd.DataFrame(c.financials(peers[x]))
        df1 = df1.rename(index={0: peers[x]})
        df = df.append(df1)

    df.dropna()

    params = list(df.columns)
    st.subheader('Create a Ratio on quarterly data')
    option1 = st.selectbox('Numerator', (params))
    option2 = st.selectbox('Denominator:',(params))

    values = df[option1]/df[option2]

    col1, col2, col3 = st.beta_columns([3, 3, 3])

    with col1:
        st.write('Ratio')
        st.write(values)

    with col2:
        st.write(option1)
        st.write(df[option1]/2)

    with col3:
        st.write(option2)
        st.write(df[option2]/2)

    st.bar_chart(values)

def fun_val(symbol):
    stock = IEXstock(API_key.IEX_API_KEY, symbol)

    st.subheader('Fundamental Data on Yearly Data')
    df = pd.DataFrame(IEX.get_valuations(symbol))
    df = df.rename(index={0: symbol})

    peers = stock.get_peers()

    for x in range(0, len(peers)):
        df1 = pd.DataFrame(IEX.get_valuations(peers[x]))
        df1 = df1.rename(index={0: peers[x]})
        df = df.append(df1)

    params = list(df.columns)
    option = st.selectbox('Data', (params))
    st.write(df[option])
    st.bar_chart(df[option])

def fun_val2(symbol):
    df2 = pd.DataFrame(IEX.get_valuations2(symbol))
    st.write(df2)


def ratio_TS(symbol, term, last):
    df = IEX.get_reported(symbol, term, last)
    df = pd.DataFrame(df['financials'])
    df = df.loc[::-1].reset_index(drop=True)
    df = df.set_index("fiscalDate")

    data = pd.DataFrame()
    params = list(df.columns)
    option1 = st.selectbox('Numerator', (params))
    data['Numerator'] = df[option1] / 2
    option2 = st.selectbox('Denominator', (params))
    data['Denominator'] = df[option2] / 2
    data['Ratio'] = data['Numerator']/data['Denominator']

    st.line_chart(data['Ratio'])
    #st.write(df)

    #df = pd.DataFrame(IEX.get_reports(symbol))
