import streamlit as st
import pandas as pd
from PIL import Image

st.write("""
# Stock Market Web Application
**Visually** show data on a stock.
""")

#image = Image.open("") #path of image
#st.image(image, use_column_width=True)

#Sidebar header create
st.sidebar.header('User Input')

#Create function to get user input
def get_input():
    start_date = st.sidebar.text_input("Start Date", "2020-01-02")
    end_date = st.sidebar.text_input("End Date", "2020-08-04")
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AMZN")
    return start_date, end_date, stock_symbol

#Create a function to get the company name
def get_company_name(symbol):
    if symbol == 'AMZN':
        return 'Amazon'
    elif symbol == 'TSLA':
        return 'Tesla'
    elif symbol == 'GOOG':
        return 'Alphabet'
    else:
        'None'

#Create a function to get proper company data and proper timeframe from user start date and end date
        def get_data(symbol, start, end):

            #Load the data
            if symbol.upper() == 'AMZN':
                df = pd.read_csv("") #path of data.cvs file
            elif symbol.upper() == 'TSLA':
                df = pd.read_csv("") #path of data.cvs file
            elif symbol.upper() == 'GOOG':
                df = pd.read_csv("") #path of data.cvs file
            else:
                df = pd.DataFrame(columns = ['Date', 'Colse', 'Open', 'Volume', 'Adj Close', 'High', 'Low'])

            #Get the date range
            start = pd.to_datetime(start)
            end = pd.to_datetime(end)

            #Set the start and end index rows both to 0
            start_row = 0
            end_row = 0

            #Start the date from the top of the data set and go down to see if the users start date is less than or equal to the date in the data set
            for i in range(0, len(df)):
                if start <= pd.to_datetime(df['Date'][i])
