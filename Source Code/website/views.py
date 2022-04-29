#store the standard route to the website
from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash, jsonify, redirect, url_for
from flask_login import  login_required, current_user
from .models import Stock, User, UserStock,Comment
from . import db
from .fy import getStockPrice1d, getCurrentPrice
from .searchform import SearchForm
import json
from .userform import UserForm, StockForm, CommentForm
from flask_mail import Mail, Message
from . import mail
import yfinance as yf
from newsapi import NewsApiClient
import time
from .alert import thread_1
# for stock prediction
import pandas as pd
import datetime as dt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from yahoo_fin import stock_info as si
from threading import *
import random

views = Blueprint('views',__name__)

#Get most gain
def stockGain():
    stockData = pd.read_csv('website\constituents.csv')

    increasedStock = []
    price = []
    for i in range(15):
        try:
            stockInfo = yf.download(random.choice(stockData['Symbol']),period="1d")
            if (stockInfo['Close'][0]>stockInfo['Open'][0]):
                increasedStock.append(stockData['Symbol'][i])
                price.append(float("{:.2f}".format(stockInfo['Close'][0])))
        except:
            pass
    return zip(increasedStock,price)

#home page
@views.route('/', methods=['GET','POST'])
def home():
    
    gainers = stockGain()

    newsapi = NewsApiClient(api_key="a63384d0482844b3bee4612ea884705c")

    #get the source of the news
    headlines =  newsapi.get_top_headlines(category="business")

    #get the list of articles
    articles = headlines['articles']

    # get information for each articles
    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range (len(articles)):
        article=articles[i]

        news.append(article['title'])
        desc.append(article['description'])
        img.append(article['urlToImage'])
        p_date.append(article['publishedAt'])
        url.append(article['url'])

    contents =zip(news, desc,img,p_date,url)
    
    
    
    return  render_template("home.html",form =SearchForm(), user=current_user, contents=contents,gainers = gainers)
#alert
@views.route('/alert/<int:id>', methods = ['GET','POST'])
def alert(id):
    form = StockForm()
    if request.method == "POST":
        stockname = request.form['stockname']
        stockprice = request.form['stockprice']
        email = request.form['email']
        if(stockname.replace(" ","") and stockprice.replace(" ","") and email.replace(" ","")):
            try:
                # creating a thread T
                T = Thread(daemon = True, target=thread_1, args=[stockname,float(stockprice),email])
                
                # starting of thread T
                T.start()    

                return redirect(url_for('views.profile'))

            except:
                flash("Some information you enter is incorrect, please try again!",category="error")
                return render_template("alert.html", form = form, user = current_user)
    else:
        return render_template("alert.html", form = form, user = current_user)


def getStockesOwned(uss):
    owned=[]
    for us in uss:
        a=Stock.query.filter(Stock.id==us.stock_id).first().name
        owned.append(a)
    return owned

def getDividends(stocks):
    dividendRates=[]
    dividendYields=[]
    dates=[]
    total=0
    for stock in stocks:
        information=yf.Ticker(stock).info
        try:
            dividendRates.append(information["dividendRate"])
            dividendYields.append(round(information["dividendYield"]*100,2))
            total=total*+information["dividendRate"]
        except:
            dividendRates.append(0)
            dividendYields.append(0)
        try:
            timestamp= dt.datetime.fromtimestamp(information["exDividendDate"])
            dates.append(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        except:
            dates.append("N/A")
    return {"dividendRates":dividendRates,"dividendYields":dividendYields,"dates":dates,"total":total}




#profile
@views.route('/profile', methods=['GET','POST'])
@login_required
def profile(): #this function will run everytime we access the view's route

    uss=UserStock.query.filter(UserStock.user_id==current_user.id).all()#user owned stock

    total=0
    for us in uss:
        total+=int(us.number_of_stock)*Stock.query.filter(Stock.id==us.stock_id).first().price
    if(request.method == "POST"):
        stock = request.form.get('stock')

        stock = stock.lstrip()

        stock=stock.split(",")
        try:
            stockName=stock[0].lower()
            price_of_stock = getStockPrice1d(stockName)
        except:
            flash("Input error!! Please try again", category = "error")
            return redirect(url_for("views.profile"))

        if(len(stock)==1):
            quantity=1
        elif(len(stock)==2):
            quantity=stock[1].lstrip()
        elif(len(stock)==3):
            quantity=stock[1].lstrip()
            price_of_stock = stock[2].lstrip()
        else:
            flash("Input error!! Please try again", category = "error")
            redirect(url_for('views.profile'))

        if(stock):
            if(Stock.query.filter_by(name=stockName).first()):
                old_stock = Stock.query.filter_by(name=stockName).first()
                old_stock.price = str(price_of_stock)
                db.session.commit()

            else:
                new_stock = Stock(name = stockName, price = str(price_of_stock))
                db.session.add(new_stock)
                db.session.commit()
            
            if(UserStock.query.filter(UserStock.user_id==current_user.id, UserStock.stock_id==Stock.query.filter(Stock.name==stockName).first().id).first()):
                flash(stockName + " is already existed in your profile")
                #flash(stockName + " is already existed in your profile", category = "error")
                q = db.session.query(Stock.id, Stock.price).filter(Stock.name == stockName).first()
                stock_to_update = UserStock.query.filter(UserStock.user_id==current_user.id,UserStock.stock_id==q[0]).first()
                stock_to_update.number_of_stock=int(stock_to_update.number_of_stock)+int(quantity)
                db.session.commit()

                total=0
                for us in uss:
                    total+=int(us.number_of_stock)*Stock.query.filter(Stock.id==us.stock_id).first().price
                
                uss=UserStock.query.filter(UserStock.user_id==current_user.id).all()#user owned stock
                stocksOwned=getStockesOwned(uss)
                dividendInfo= getDividends(stocksOwned)

                flash("Stock updated!", category = "success")
                return  render_template("profile.html", form = SearchForm(), user = current_user, uss=uss, Stock=Stock,total=total,dividendInfo=dividendInfo,stocksOwned=stocksOwned)# return the html file that we want to render to the website

            elif (len(stockName)<0):
                flash("stock name is too short!", category = "error")

            else:
                #if the stock is not in the stock database, add the stock to the stocks table first
                
                q = db.session.query(Stock.id, Stock.price).filter(Stock.name == stockName).first()
                
                new_UserStock=UserStock(user_id=current_user.id, stock_id=q[0],number_of_stock=quantity)
                db.session.add(new_UserStock)
                db.session.commit()

                uss=UserStock.query.filter(UserStock.user_id==current_user.id).all()#user owned stock

                total=0
                for us in uss:
                    total+=int(us.number_of_stock)*Stock.query.filter(Stock.id==us.stock_id).first().price
                uss=UserStock.query.filter(UserStock.user_id==current_user.id).all()#user owned stock
                stocksOwned=getStockesOwned(uss)
                dividendInfo= getDividends(stocksOwned)
                flash("new Stock added!", category = "success")
                return  render_template("profile.html", form = SearchForm(), user = current_user, uss=uss, Stock=Stock,total=total,dividendInfo=dividendInfo,stocksOwned=stocksOwned)# return the html file that we want to render to the website
        else:
            uss=UserStock.query.filter(UserStock.user_id==current_user.id).all()#user owned stock
            stocksOwned=getStockesOwned(uss)
            dividendInfo= getDividends(stocksOwned)
            return  render_template("profile.html", form = SearchForm(), user = current_user,uss=uss,Stock=Stock,total=total,dividendInfo=dividendInfo,stockOwned=stocksOwned)# return the html file that we want to render to the website
    uss=UserStock.query.filter(UserStock.user_id==current_user.id).all()#user owned stock
    stocksOwned=getStockesOwned(uss)
    dividendInfo= getDividends(stocksOwned)
    return  render_template("profile.html", form = SearchForm(), user = current_user,uss=uss,Stock=Stock,total=total,dividendInfo=dividendInfo,stocksOwned=stocksOwned)# return the html file that we want to render to the website


# delete stock name
@views.route('delete-stock', methods=['POST'])
def delete_stock():
    stock = json.loads(request.data)
    stockId = stock['stock_id']
    stock = UserStock.query.filter(UserStock.user_id==current_user.id, UserStock.stock_id==stockId).first()
    if (stock):
        flash(Stock.query.filter(Stock.id==stockId).first().name + " stock is successfully removed from your watchlist")
        db.session.delete(stock)
        db.session.commit()
    return jsonify({})


#update user information
@views.route('/update/<int:id>', methods = ['GET','POST'])
def updateProfile(id):
    form = UserForm()
    user_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        newfirstname = request.form['firstname']
        newlastname = request.form['lastname']
        newemail = request.form['email']
        if(newemail.lstrip()):
            user_to_update.email = request.form['email']
        if(newfirstname.lstrip()):
            user_to_update.firstname = request.form['firstname']
        if(newlastname.lstrip()):
            user_to_update.lastname  = request.form['lastname']
        try:
            db.session.commit()
            flash("Your information has been updated!", category = "success")
            return render_template("profile.html",form = form, user = current_user, user_to_update = user_to_update)
        except:
            flash("There is an ERROR!!!. We cannot update your information. Please try again", category = "error")
    
    else:
        return render_template("update.html", form = form, user = current_user, user_to_update = user_to_update)

@views.route('/comment/<string:stockName>', methods = ['GET','POST'])
def addComment(stockName):
    form = CommentForm()
    if request.method == "POST":
        text = request.form['comment']
        email = request.form['email']
        rating = request.form['rating']
        newComment = Comment(email = email,stockName = stockName.lower(), comment=text, rating =rating)
        db.session.add(newComment)
        db.session.commit()
        return redirect(url_for("views.search",stock=stockName))
    else:
        return render_template("comment.html", form = form, user = current_user)
    #stockComment = Comment(stockName=stockName,comment=)
    

@views.route('/delete/<int:id>', methods = ['GET','POST'])
def delete(id):
    try:
        userStocks=UserStock.query.filter(UserStock.user_id==current_user.id).all()
        for stock in userStocks:
            db.session.delete(stock)
        User.query.filter_by(id=id).delete()
        db.session.commit()
        print("We have deleted your account")
        flash("We have deleted your account", category = "success")
    except:
        print("There is an ERROR!!!")
        flash("There is an ERROR!!!. We cannot delete your account. Please try again", category = "error")
    
    return redirect(url_for('views.home'))

#send message
@views.route('/contactus', methods=['GET','POST'])
def message():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        message = request.form.get('message')
        msg = Message(subject = f'Mail from {name}', body = f'{message}', sender = email, recipients = ['fiaaonline@gmail.com'])
        mail.send(msg)
        flash("Thank you for contact us.", category = "success")
        flash("Your message was sent. We will contact you soon.", category = 'error')
    
    return render_template("contactus.html", form = SearchForm(), user = current_user)

#Pass stuff to Navbar
@views.context_processor
def base():
    form = SearchForm()
    return dict(form = form)# we need to let the base.html know that search has a form

price=[]
dates=[]
#search
@views.route('/search', methods=["GET","POST"])
def search():
    try:
        form = SearchForm()
        if (form.validate_on_submit()):
            searched = form.search.data
            comments = Comment.query.filter(Comment.stockName==searched.lower()).all()
            stats = stockInfo(searched,"1d")
            recomendation = information(searched)
            info = getGeneralInfo(searched)
            return render_template("search.html",form=form, user=current_user, searched= searched,dates=json.dumps(stats[1]),money=json.dumps(stats[0]),Info=info,recomend=recomendation, comments=comments)
        else:
            searched = request.args.get('stock')
            comments = Comment.query.filter(Comment.stockName==searched.lower()).all()
            stats = stockInfo(searched,"1d")
            recomendation= information(searched)
            info = getGeneralInfo(searched)
            return render_template("search.html",form=form, user=current_user, searched= searched,dates=json.dumps(stats[1]),money=json.dumps(stats[0]),Info=info,recomend=recomendation, comments=comments)
        
    except:
        flash("The stock you want is not available!!", category = 'error')
        return redirect(url_for('views.home'))

@views.route('/prices',methods=["GET","POST"])
def prices():
    info = stockInfo(request.args.get('stock'),request.args.get('time'))
    # GETTING THE DATES
    prices=info[0]
    dates = info[1]
    data={"dates":dates,"prices":prices}
    return json.dumps(data)


@views.route('/prediction',methods=["GET","POST"])
def prediction():
    return json.dumps(machinelearningPrediction(request.args.get('stock')))

@views.route('/compare',methods=["GET","POST"])
def compare():
    try:
        stock = request.args.get('stock')
        ticker = getGeneralInfo(stock)
    except:
        return json.dumps({})
    return json.dumps(ticker)



def stockInfo(stock,time):
    if time=='1d':
        #information = yf.history(tickers=stock, period=time, interval='5m')
        information=yf.Ticker(stock).history(period=time,interval='5m')
    elif time=='3mo'or time=='6mo':
        information = yf.download(tickers=stock, period=time, interval='1h')
    elif time=='1y':
        information = yf.download(tickers=stock, period=time, interval='1d')
    else:
        information = yf.download(tickers=stock, period=time, interval='1wk')
    information=information.dropna()
    price=information['Open'].tolist()
    dates=[]
    for i in information.index:
        dates.append(i.strftime('%Y-%m-%d %X'))
    return[price,dates]

def information(stock):
    ticker= yf.Ticker(stock)
    if ticker.recommendations.empty :
        return {'dates':[],'firms':[],'grades':[]}
    information=ticker.recommendations.tail(5)
    dates=[]
    for i in information.index:
        dates.append(i.strftime('%Y-%m-%d %X'))
    firms= information['Firm'].tolist()
    grade=information['To Grade'].tolist()
    return {'dates':dates,'firms':firms,'grades':grade}

def getGeneralInfo(stock):
    information= yf.Ticker(stock).info
    words=['longName','symbol','longBusinessSumary']
    decimals=['currentPrice','fiftyTwoWeekHigh','fiftyTwoWeekLow','fiftyDayAverage','twoHundredDayAverage','trailingPE','forwardPE',
    'priceToSalesTrailing12Months','priceToBook','returnOnAssets','returnOnEquity','revenueGrowth','trailingEps']
    numbers=['marketCap']
    for word in words:
        if word not in information:
            information[word]='N/A'
    for decimal in decimals:
        if decimal not in information:
            information[decimal]='N/A'
        elif information[decimal]==None:
            information[decimal]='N/A'
        else:
            information[decimal]=round(information[decimal],2)
    for number in numbers:
        if number not in information:
            information[number]='N/A'
        else:
            information[number]=f"{information[number]:,}"
    return information


def create_dataset(dataset,time_step=1):
    dataX,dataY=[],[]
    for i in range(len(dataset)-time_step): 
        a=dataset[i:(i+time_step),0] 
        dataX.append(a)
        dataY.append(dataset[i+time_step,0])
    return np.array(dataX),np.array(dataY)

def machinelearningPrediction(stock):
    today = dt.date.today()
    yesterday = today - dt.timedelta(days = 1)
    start=yesterday-dt.timedelta(days=500)
    start=start.strftime("%Y-%m-%d")
    yesterday=yesterday.strftime("%Y-%m-%d")
    # load data
    data=yf.download(stock,start=start,end=yesterday)
    df1=data.reset_index()['Adj Close']
    #transform the data
    scaler = MinMaxScaler(feature_range=(0,1))
    df1=scaler.fit_transform(np.array(df1).reshape(-1,1))
    #splitting dataset into train and test 
    training_size=int(len(df1)*0.65)
    test_size = len(df1)-training_size
    train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]
    #reshape into x=t,t+1,t+2,t+3 and Y=t+4
    time_step=30
    x_train,y_train=create_dataset(train_data,time_step)
    x_test,y_test=create_dataset(test_data,time_step)
    # reshape input to be [samples,time steps,features] which is required by lstm
    x_train = x_train.reshape(x_train.shape[0],x_train.shape[1],1)
    x_test = x_test.reshape(x_test.shape[0],x_test.shape[1],1)
    #creatin model
    model=Sequential()
    #input shape the one we are passing in 
    model.add(LSTM(50,return_sequences=True,input_shape=(time_step,1)))
    model.add(LSTM(50,return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error',optimizer='adam')
    model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=30,batch_size=10,verbose=1)
    # getting what we want
    x_input=test_data[len(test_data)-time_step:].reshape(1,-1)
    temp_input=list(x_input)
    temp_input=temp_input[0].tolist()
    lst_output=[]
    n_steps=time_step
    i=0
    while(i<30):
        if(len(temp_input)>time_step):
            #print(temp_input)
            x_input=np.array(temp_input[1:])
            #print("{} day input {}".format(i,x_input))
            x_input=x_input.reshape(1,-1)
            x_input = x_input.reshape((1, n_steps, 1))
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input=temp_input[1:]
            #print(temp_input)
            lst_output.extend(yhat.tolist())
            i=i+1
        else:
            x_input = x_input.reshape((1, n_steps,1))
            yhat = model.predict(x_input, verbose=0)
            #print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            #print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i=i+1
    answer=[]
    past=(scaler.inverse_transform(df1[len(df1)-time_step:]))
    future=(scaler.inverse_transform(lst_output))
    for price in past:
        answer.append(price[0])
    for price in future:
        answer.append(price[0])
    return answer
    

    



