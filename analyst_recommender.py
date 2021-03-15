import random
import numpy as np
import pandas as pd
import yfinance as yf
#import datetime as dt
import streamlit as st

st.title('Analyst Recommender')
with st.beta_expander('purpose'):
    st.write('This was something that I stumbled upon when looking at the yfinance \
             essentially what it does is look at analysts results to and then compares \
                 it to similar stocks to find the one that is the most similar. A majority\
                     of this project is to test the Streamlit app.')

def recommender(symbol):
    
    tickerSymbol = symbol
    tickerData = yf.Ticker(tickerSymbol)
    recommendations = tickerData.recommendations
    
    recommendations.drop_duplicates(subset = "Firm", keep = 'last', inplace = True)
    
    recommendations['score'] = np.nan
    
    for i in range(len(recommendations)):
        
        #print(recommendations['To Grade'][i])
        
        if recommendations['To Grade'][i] == "Buy" or recommendations['To Grade'][i] == "Outperform" or recommendations['To Grade'][i] == "Overweight" or recommendations['To Grade'][i] == "Strong Buy" or recommendations['To Grade'][i] == "Market Outperform" or recommendations['To Grade'][i] == "Positive":
            recommendations['score'][i] = 1
            
        if recommendations['To Grade'][i] == "Neutral" or recommendations['To Grade'][i] == "Hold" or recommendations['To Grade'][i] == "Market Perform" or recommendations['To Grade'][i] == "Sector Weight" or recommendations['To Grade'][i] == "Perform" or recommendations['To Grade'][i] == "Sector Perform" or recommendations['To Grade'][i] == "Equal-Weight":
            recommendations['score'][i] = 0
            
        if recommendations['To Grade'][i] == "Underperform" or recommendations['To Grade'][i] == "Sell" or recommendations['To Grade'][i] == "Negative" or recommendations['To Grade'][i] == "Underweight":
            recommendations['score'][i] = -1
            
    recommendations = recommendations.reset_index(drop = True)
    recommendations.index = recommendations['Firm']
    recommendations = recommendations.drop(columns = ['To Grade', 'From Grade', 'Action', 'Firm'])
    recommendations = recommendations.rename(columns = {"score": str(symbol)})
    
    return recommendations

st.header("company's recommendations")
ticker_input = st.text_input('Please enter your company ticker here:')
status_radio = st.radio('Please click Search when you are ready.', ('Entry', 'Search'))

if status_radio == 'Search':
    
    tickerSymbol = ticker_input
    tickerData = yf.Ticker(tickerSymbol)
    recommendations = tickerData.recommendations
    st.dataframe(recommendations)
    
    ticker = ticker_input
    
    st.header("Enter in how many randomly chosen stocks")
    number_input = st.number_input('Please enter number here you can type it in:')
    number_input = int(number_input)
    print(type(number_input))
    number_radio = st.radio("Please click Search when you've picked a number", ('Entry', 'Search'))
    
    if number_radio == "Search":
    
        def get_tickers(number, ticker):
            
            table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
            df = table[0]
            
            tickers = df['Symbol'].tolist()
            tickers.remove("BRK.B")
            tickers.remove("BF.B")
            tickers.remove("SLG")
            tickers.remove("VNT")
            
            
            difference = len(tickers) - number
            
            random_ints = random.sample(range(len(tickers)), difference)
            random_ints = sorted(random_ints, reverse= True)
            
            for i in range(len(random_ints)):
                
                drop_value = tickers[random_ints[i]]
                tickers.remove(drop_value)
                
            for j in range(len(tickers)):
                if tickers[j] == ticker:
                    tickers.remove(ticker)
                
            return tickers
        
        tickers = get_tickers(number_input, ticker)
        result = recommender(ticker)
        add = pd.DataFrame()
        
        for i in range(len(tickers)):
            
            st.write('working on', tickers[i])
            
            add = recommender(tickers[i])
            result = pd.concat([result, add], axis = 1)
        
        analyst_count = len(result[str(ticker)].dropna())
        result = result[:analyst_count]
        result = result.append(pd.Series(name = "score"))
        
        for j in result.columns:
            
            score_value = result[str(j)].dropna()
            score_value = int(score_value.sum())
            result[str(j)]['score'] = score_value 
            
        scores = result.values.tolist()[-1]
        scores_comparison = scores[1:]
        max_score = max(scores_comparison)
        
        similar_stock = ''
        
        for k in range(len(scores)):
            
            if scores[k] == max_score:
                
                similar_stock = result.columns[k]
                
        similar_score = round(max_score / result[str(ticker)][len(result) - 1] * 100,2)
        st.write("the stock that is similar is", similar_stock, "and is ", similar_score,"% similar by analysts ratings" )