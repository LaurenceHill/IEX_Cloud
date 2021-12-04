
#Library Funcitons
import streamlit as st # must pip install module
import requests
import pandas as pd
import numpy as np
import matplotlib
from datetime import datetime
import pyEX
import json

#Created Functions
from IEXstock import IEXstock
import IEXstock as IEX
import API_key
import Fundamentals
import IS
import BS
import quants
import pizza
import cash_flow
from datetime import datetime
import redis_function
import iexfinance
import altair as alt

# Side Bar
st.set_page_config(layout="wide")
symbol = st.sidebar.text_input('symbol', value='AAPL')
# Link to IEX self function
stock = IEXstock(API_key.IEX_API_KEY, symbol)
# select Side Bar Category
screen = st.sidebar.selectbox('View', ('Overview', 'News',
                                       'Financials: Income Statement', 'Financials: Balance Sheet', 'Financials: Cash Flow', 'Financials: Reported',
                                       'Valuations: Fundamentals','Valuations: Models', 'Valuations: Time-series',
                                       'Ratio: Construction','Ratio: Company Comparison',
                                       ))
# Dashboard
st.title(screen)# write catergory as title

#IEX cloud function
c = pyEX.Client(api_token=API_key.IEX_API_KEY)

# If command for side bar
if screen == 'Overview':
    logo = stock.get_logo()

    logo = stock.get_logo()
    company_info = stock.get_company_info()

    est = stock.get_estimates()
    sector_p = stock.get_sector_p()
    insider = stock.get_insiderSum()
    price = stock.get_quote()

    col1, col2 = st.beta_columns([3, 8])

    with col1:
        st.image(logo['url'])
        st.write('Current Price:')
        st.write(price)

        st.write('Analyst Target:')
        st.write(est[0]['marketConsensusTargetPrice'])
        st.write('Consensus Date:', est[0]['consensusDate'])
        st.write('Analyst count:', est[0]['analystCount'])


    with col2:
        st.subheader(company_info['companyName'])
        st.write('CEO: ', company_info['CEO'])
        st.write(company_info['website'])
        st.subheader('Company Description')
        st.write(company_info['description'])
        st.subheader('Industry and Tags')
        st.write(company_info['industry'])
        st.write(company_info['tags'])

        st.subheader('Insider Transaction - Last 6 months')
        st.write('Last 5 Transactions:')
        for x in range(0,5):
            st.write(insider[x]['fullName'], insider[x]['netTransacted'])

if screen == 'News':
    news = stock.get_company_news()
    for article in news:
        st.subheader(article['headline'])
        st.write(article['url'])
        st.write(article['summary'])
        st.image(article['image'])
        dt = datetime.utcfromtimestamp(article['datetime'] / 1000).isoformat()
        st.write(f"Posted by {article['source']} at {dt}")

if screen == 'Financials: Income Statement':

    df = pd.DataFrame(IS.income_statement(symbol))
    params = list(df.columns)

    option = st.selectbox('Income Statement: Category 1', params)
    option2 = st.selectbox('Income Statement: Category 2', params)
    option3 = st.selectbox('Income Statement: Category 3', params)

    peers = stock.get_peers()
    peers.insert(0, symbol)

    st.write('Click for Comparison')
    for x in range(0, len(peers)):
        if st.button(peers[x]):
            IS.income_statement_comparison(symbol, peers[x],option)
            IS.income_statement_comparison(symbol, peers[x], option2)
            IS.income_statement_comparison(symbol, peers[x], option3)

if screen == 'Financials: Balance Sheet':

    BS.bs_stack_chart(symbol)

    df = pd.DataFrame(BS.balance_sheet(symbol))
    params = list(df.columns)

    option = st.selectbox('Balance Sheet: Category 1', params)
    option2 = st.selectbox('Balance Sheet: Category 2', params)
    option3 = st.selectbox('Balance Sheet: Category 3', params)

    peers = stock.get_peers()
    peers.insert(0, symbol)

    peers = stock.get_peers()
    peers.insert(0, symbol)
    st.write('Click for Comparison')
    for x in range(0, len(peers)):
        if st.button(peers[x]):
            BS.balance_sheet_comparison(symbol, peers[x],option)
            BS.balance_sheet_comparison(symbol, peers[x], option2)
            BS.balance_sheet_comparison(symbol, peers[x], option3)

if screen == 'Financials: Cash Flow':

    cash_flow.CF_stack_chart(symbol)

    df = pd.DataFrame(cash_flow.cash_flow(symbol))
    params = list(df.columns)

    option = st.selectbox('Cash Flow: Category 1', params)
    option2 = st.selectbox('Cash Flow: Category 2', params)
    option3 = st.selectbox('Cash Flow: Category 3', params)

    peers = stock.get_peers()
    peers.insert(0, symbol)

    peers = stock.get_peers()
    peers.insert(0, symbol)
    st.write('Click for Comparison')
    for x in range(0, len(peers)):
        if st.button(peers[x]):
            cash_flow.cash_flow_comparison(symbol, peers[x],option)
            cash_flow.cash_flow_comparison(symbol, peers[x], option2)
            cash_flow.cash_flow_comparison(symbol, peers[x], option3)

if screen == 'Financials: Reported':
    st.subheader('Financials Reported')
    report = '10-Q'
    report = st.selectbox('Report type:', ('10-k', '10-Q'))
    if report == '10-k':
        periods = st.number_input('Number of Years',min_value=3, max_value=10)
    elif report == '10-Q':
        periods = st.number_input('Number of Quarters',min_value=4,max_value=40)

    df = pd.DataFrame(IEX.get_reports(symbol, report, periods))
    params = list(df.columns)
    df = df.loc[::-1].reset_index(drop=True)

    option1 = st.selectbox('Income Statement: Graph 1', params)
    st.line_chart(df[option1])
    st.write('Filing Date: Start', datetime.fromtimestamp(df['dateFiled'].iloc[0] / 1e3).strftime('%d-%m-%y'))
    st.write('Filing Date: End', datetime.fromtimestamp(df['dateFiled'].iloc [-1]/1e3).strftime('%d-%m-%y'))

    option2 = st.selectbox('Income Statement: Graph 2', params)
    st.line_chart(df[option2])
    st.write('Filing Date: Start', datetime.fromtimestamp(df['dateFiled'].iloc[0] / 1e3).strftime('%d-%m-%y'))
    st.write('Filing Date: End', datetime.fromtimestamp(df['dateFiled'].iloc [-1]/1e3).strftime('%d-%m-%y'))

    st.write(df)

    st.header('Long Term Data')
    cash_flow.CF(symbol, 8, 24)


if screen == 'Valuations: Models':

    option = st.selectbox('Models:',
                          ('Dupont', 'CAGR', 'FCFE discount Model', 'Gordon Growth Model', '2 Stage Growth Model',
                           'DDM'))

    if option == 'Dupont':
        st.header('DuPont: 5 Phase')
        df = pd.DataFrame(redis_function.funVal(symbol, 12))
        # st.write(df)
        df = df.set_index('filingDate')

        options = st.multiselect('Dupont:', (
        'ebitToRevenue', 'assetTurnover', 'assetsToEquity', 'interestBurden', 'taxBurden', ))

        valuations = df[options]
        if valuations.empty:
            st.write(' ')
        else:
            #st.write(valuations)
            st.line_chart(valuations)

        dupont = df['ebitToRevenue']*df['assetTurnover']*df['assetsToEquity']*df['interestBurden']*df['taxBurden']
        st.subheader("DuPont: 5 Phase")
        st.line_chart(dupont)

    if option == 'CAGR':
        option = st.selectbox('Income Statement: Category',
                              ('totalRevenue', 'grossProfit', 'operatingIncome', 'operatingExpense', 'netIncome'))
        quants.CAGR(symbol, option)

    # if option == 'DuPont Manual':
    #     st.header('Dupont: 3 Phase')
    #     st.write('ROE = Net Income Margin x Asset Turnover x Financial Leverage')
    #     st.write('ROE = Net Income/Revenue x Revenue/Total Assets x Total Assets/Total Equity')
    #     col1, col2 = st.beta_columns([8, 8])
    #
    #     with col1:
    #         income_statement = stock.get_financials()
    #         net_income = income_statement['financials'][0]['netIncome']
    #         revenue = income_statement['financials'][0]['revenue']
    #         ebit = income_statement['financials'][0]['ebit']
    #         equity = income_statement['financials'][0]['shareholderEquity']
    #         total_assets = income_statement['financials'][0]['totalAssets']
    #
    #         st.subheader('Varibles')
    #         st.write('Net Income:', net_income)
    #         st.write('Revenue:', revenue)
    #         st.write('Total Assets:', total_assets)
    #         st.write('Equity:', equity)
    #
    #         st.subheader('Formula')
    #         st.write('Net Income Margin ', net_income/revenue)
    #         st.write('Asset Turnover ', revenue/total_assets)
    #         st.write('Financial Leverage ', total_assets/equity)
    #
    #         ROE = round(float((net_income/revenue)*(revenue/total_assets)*(total_assets/equity)*100),2)
    #
    #         st.write('ROE(%) =', ROE)
    #
    #     with col2:
    #         st.write('Press for Comparison')
    #         peers = stock.get_peers()
    #         for x in range(0, len(peers)):
    #             if st.button(peers[x]):
    #                 income_statement = c.financials(peers[x])
    #                 #st.write(income_statement)
    #                 net_income = income_statement[0]['netIncome']
    #                 revenue = income_statement[0]['revenue']
    #                 ebit = income_statement[0]['ebit']
    #                 equity = income_statement[0]['shareholderEquity']
    #                 total_assets = income_statement[0]['totalAssets']
    #
    #                 st.subheader('Varibles')
    #                 st.write('Net Income:', net_income)
    #                 st.write('Revenue:', revenue)
    #                 st.write('Total Assets:', total_assets)
    #                 st.write('Equity:', equity)
    #
    #                 st.subheader('Formula')
    #                 st.write('Net Income Margin ', net_income / revenue)
    #                 st.write('Asset Turnover ', revenue / total_assets)
    #                 st.write('Financial Leverage ', total_assets / equity)
    #
    #                 ROE = round(float((net_income / revenue) * (revenue / total_assets) * (total_assets / equity) * 100), 2)
    #
    #                 st.write('ROE(%) =', ROE)
    # elif option == 'DDM - Dividend Discount Model':
    #     st.header('DDM - Dividend Discount Model')
    #
    #
    # # stats = stock.get_stats()
    # # st.write(stats)

if screen == 'Valuations: Fundamentals':
    df = pd.DataFrame(redis_function.funVal(symbol, 12))
    #st.write(df)
    df = df.set_index('filingDate')
    params = list(df.columns)

    options = st.multiselect('Parameter:',(params))

    valuations = df[options]
    if valuations.empty:
        st.write(' ')
    else:
        st.write(valuations)
        st.line_chart(valuations)

if screen == 'Valuations: Time-series':
    df = pd.DataFrame(redis_function.funVal(symbol,12))
    #st.write(df)
    s_date = df['filingDate'][len(df)-1]
    df = df.set_index('filingDate')

    options = st.multiselect('Valuations & Yields:', ('evToSales', 'evToEbit', 'evToEbitda', 'pToE', 'pToBv', 'fcfYield', 'dividendYield', 'earningsYield'))

    valuations = df[options]
    if valuations.empty:
        st.write(' ')
    else:
        #st.write(valuations)
        st.line_chart(valuations)

    options_g = st.multiselect('Growth:', ('revenueGrowth','netIncomeGrowth', 'ebitGrowth', 'ebitdaGrowth',
                                           'freeCashFlowGrowth', 'operatingCashFlowGrowth', 'netWorkingCapitalGrowth'))
    growth = df[options_g]
    if growth.empty:
        st.write(' ')
    else:
        #st.write(growth)
        st.line_chart(growth)

    options_m = st.multiselect('Margin:', ('ebitToRevenue', 'ebitMargin', 'freeCashFlowToRevenue', 'netIncomeToRevenue',
                                           'operatingCFToRevenue', 'operatingIncomeToRevenue','profitGrossToRevenue',
                                           'sgaToRevenue'))
    margin = df[options_m]
    if margin.empty:
        st.write(' ')
    else:
        #st.write(margin)
        st.line_chart(margin)

    options_r = st.multiselect('Returns:', ('roic', 'roce'))
    returns1 = df[options_r]
    if returns1.empty:
        st.write(' ')
    else:
        #st.write(returns1)
        st.line_chart(returns1)

    options_p = st.multiselect('Price:', ('pToE', 'ptoBV', 'priceToRevenue'))
    returns = df[options_p]
    if returns.empty:
        st.write(' ')
    else:
        #st.write(returns)
        st.line_chart(returns)

    chart = stock.get_chart()

    chart = pd.DataFrame(chart, columns=['date', 'close'])
    # df[df['date'] < s_date] #drop after filing date
    chart = chart.rename(columns={'date': 'index'}).set_index('index')
    st.line_chart(chart,use_container_width=True)

    # brush = alt.selection(type='interval', encodings=['x'])
    #
    # base = alt.Chart(chart).mark_area().encode(
    #     x='date',
    #     y='close'
    # ).properties(
    #     width=1200,
    #     height=300
    # )
    #
    # upper = base.encode(
    #     alt.X('date:T', scale=alt.Scale(domain=brush))
    # )
    #
    # lower = base.properties(
    #     height=80
    # ).add_selection(brush)
    #
    # upper & lower



if screen == 'Ratio: Company Comparison':
    pizza.pizza(symbol)

if screen == 'Ratio: Construction':
    pizza.ratio_TS(symbol,0,8)







#Must edit still

#if screen == 'Fundamental Ratios':
#      st.write('fun')
#      pizza.fun_val(symbol)
#      df = pizza.fun_val2(symbol)
#      df = pd.DataFrame(df)
#      params = list(df.columns)
#      df = df.loc[::-1].reset_index(drop=True)
#      df = df.set_index("fiscalDate")
#      option1 = st.selectbox('Income Statement: Graph 1', params)
#      st.line_chart(df[option1])

#Past Projects
if screen == 'Graphical Interface':
    periods = 4
    cash_flow = c.cashFlow(symbol,period='annual',last=periods)
    #income_statement = c.incomeStatement(symbol, period='quarter', last=periods)
    #balance_sheet = c.balanceSheet(symbol, period='quarter', last=periods)

    array_y = []
    array_x = []
    #array_y = pd.DataFrame()
    #array_x = pd.DataFrame()

    for x in range(0,periods):
        array_y.append(-cash_flow[(periods-1)-x]['capitalExpenditures'])
        array_x.append(cash_flow[(periods-1)-x]['cashFlow'])
        #st.write(cash_flow[x]['cashFlowFinancing'])

    st.line_chart(array_y)
    st.line_chart(array_x)

    st.bar_chart(array_y)
    st.bar_chart(array_x)

    st.write(cash_flow)
    #st.write(income_statement)
    #st.write(cash_flow)

if screen == 'Analysts':
    analysts = stock.get_analyst()
    st.write(analysts)

if screen == 'Financials':
    periods = 12
    #financials = c.fundamentals(symbol, period='annual')
    #financials_val = c.fundamentalValuations(symbol)

    #st.write(financials_val)

if screen == 'Revenue Growth':

    periods = 12
    income_statement = c.incomeStatement(symbol,period='quarter',last=periods)
    income_statement1 = c.incomeStatement(symbol1, period='quarter', last=periods)

    total_revenue = []
    total_date = []
    total_revenue1 = []
    total_date1 = []

    df = pd.DataFrame(columns={'date', 'revenue'})
    df1 = pd.DataFrame(columns={'date', 'revenue'})

    for x in range(0,12):
        total_revenue.append(income_statement[periods-1-x]['totalRevenue'])
        total_date.append(income_statement[periods - 1 - x]['fiscalDate'])

    for x in range(0, 12):
        total_revenue1.append(income_statement1[periods - 1 - x]['totalRevenue'])
        total_date1.append(income_statement1[periods - 1 - x]['fiscalDate'])


        #df['date'][x] = income_statement[periods - 1 - x]['fiscalDate']

        #df['date'].append(income_statement[periods - 1 - x]['fiscalDate'])
        #df['revenue'].append(income_statement[periods - 1 - x]['totalRevenue'])


    #st.line_chart(total_revenue)
    #st.write(total_date)

    df['date'] = pd.Series(total_date)
    df['revenue'] = pd.Series(total_revenue)
    helpdf = df.rename(columns={'date': 'index'}).set_index('index')

    df1['date'] = pd.Series(total_date)
    df1['revenue'] = pd.Series(total_revenue1)
    df1 = df1.rename(columns={'date': 'index'}).set_index('index')

    st.line_chart(df)
    st.line_chart(df1)




