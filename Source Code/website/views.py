#store the standard route to the website
from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash, jsonify, redirect, url_for
from flask_login import  login_required, current_user
from .models import Stock, User, UserStock
from . import db
from .fy import getStockPrice1d, getCurrentPrice
from .searchform import SearchForm
import json
from .userform import UserForm
from flask_mail import Mail, Message
from . import mail
import yfinance as yf
from newsapi import NewsApiClient

views = Blueprint('views',__name__)

#home page
@views.route('/', methods=['GET','POST'])
def home():
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

    return  render_template("home.html",form =SearchForm(), user=current_user, contents=contents)

#profile
@views.route('/profile', methods=['GET','POST'])
@login_required
def profile(): #this function will run everytime we access the view's route
    id= db.session.query(User.id).filter(User.email==current_user.email)

    uss=UserStock.query.filter(UserStock.user_id==id).all()#user owned stock


    if(request.method == "POST"):

        stock = request.form.get('stock')

        stock = stock.lstrip()

        stock=stock.split(",")

        stockName=stock[0].lower()

        quantity=stock[1].lstrip()

        if(stock):
            if(db.session.query(UserStock.stock_id).filter(Stock.name == stockName).first()):
                print(stockName + " is already existed in your profile")
                flash(stockName + " is already existed in your profile", category = "error")

            elif (len(stockName)<0):
                flash("stock name is too short!", category = "error")

            else:
                #if the stock is not in the stock database, add the stock to the stocks table first
                if(Stock.query.filter_by(name=stockName).first()):
                    print("Stock already in")
                else:
                    new_stock = Stock(name = stockName, price = str(getStockPrice1d(stockName)))
                    db.session.add(new_stock)
                    db.session.commit()

                q = db.session.query(Stock.id, Stock.price).filter(Stock.name == stockName).first()
                
                print(current_user.email)
                new_UserStock=UserStock(user_id=id, stock_id=q[0],number_of_stock=quantity)
                db.session.add(new_UserStock)
                db.session.commit()

                uss=UserStock.query.filter(UserStock.user_id==id).all()#user owned stock

                flash("new Stock added!", category = "success")
                return  render_template("profile.html", form = SearchForm(), user = current_user, uss=uss, Stock=Stock)# return the html file that we want to render to the website
        else:
            return  render_template("profile.html", form = SearchForm(), user = current_user,uss=uss,Stock=Stock)# return the html file that we want to render to the website

    return  render_template("profile.html", form = SearchForm(), user = current_user,uss=uss,Stock=Stock)# return the html file that we want to render to the website

# delete stock name
@views.route('delete-stock', methods=['POST'])
def delete_stock():
    stock = json.loads(request.data)
    stockId = stock['stockId']
    stock = Stock.query.get(stockId)
    if (stock):
        if (stock.user_id == current_user.id):
            flash(stock.name + " stock is successfully removed from your watchlist")
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



@views.route('/delete/<int:id>', methods = ['GET','POST'])
def delete(id):
    try:
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
    form =SearchForm()
    if (form.validate_on_submit()):
        searched = form.search.data
        stats = stockInfo(searched,"1d")
        values= stats[0]
        dates=stats[1]
        Info = information(searched)
        return render_template("search.html",form=form, user=current_user, searched= searched,dates=json.dumps(dates),money=json.dumps(values),Info=Info[0],recomend=Info[1])
    else:
        info = stockInfo(request.args.get('stock'),request.args.get('time'))
        # GETTING THE DATES
        prices=info[0]
        dates = info[1]
        data={"dates":dates,"prices":prices}
        return json.dumps(data)

def stockInfo(stock,time):
    information=''
    if time=='1d':
        information = yf.download(tickers=stock, period=time, interval='1m')
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
    information=ticker.recommendations.tail(5)
    dates=[]
    for i in information.index:
        dates.append(i.strftime('%Y-%m-%d %X'))
    firms= information['Firm'].tolist()
    grade=information['To Grade'].tolist()
    return [ticker.info,{'dates':dates,'firms':firms,'grades':grade}]



