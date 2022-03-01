#store the standard route to the website
from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash, jsonify, redirect, url_for
from flask_login import  login_required, current_user
from .models import Stock, User
from . import db
from .fy import getStockPrice1d, getCurrentPrice
from .searchform import SearchForm
import json
from .userform import UserForm
from flask_mail import Mail, Message
from . import mail
import yfinance as yf
import random

views = Blueprint('views',__name__)

#home page
@views.route('/', methods=['GET','POST'])
def home():
    return  render_template("home.html",form =SearchForm(), user=current_user)

#profile
@views.route('/profile', methods=['GET','POST'])
@login_required
def profile(): #this function will run everytime we access the view's route
    if(request.method == "POST"):
        stock = request.form.get('stock')

        stock = stock.lstrip()

        if(stock):
            if(Stock.query.filter_by(name = stock).first()):
                flash(stock + " is already existed in your stock list", category = "error")

            elif (len(stock)<0):
                flash("stock name is too short!", category = "error")

            else:
                new_stock = Stock(name = stock, price = str(getStockPrice1d(stock)),user_id = current_user.id)
                db.session.add(new_stock)
                db.session.commit()
                flash("new Stock added!", category = "success")
                return  render_template("profile.html", form = SearchForm(), currentprice = getCurrentPrice(stock), user = current_user)# return the html file that we want to render to the website
        else:
            return  render_template("profile.html", form = SearchForm(), user = current_user)# return the html file that we want to render to the website

    return  render_template("profile.html", form = SearchForm(), user = current_user)# return the html file that we want to render to the website

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
        Stock.query.filter_by(user_id=id).delete()
        User.query.filter_by(id=id).delete()
        db.session.commit()
        flash("We have deleted your account", category = "success")
    except:
        flash("There is an ERROR!!!. We cannot delete your account. Please try again", category = "error")
    
    return redirect(url_for('views.home'))

#send message
@views.route('/contactus', methods=['GET','POST'])
def message():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        message = request.form.get('message')
        msg = Message(subject = f'Mail from {name}', body = f'{message}', sender = email, recipients = ['ropofo6438@yks247.com'])
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
        price = getStockPrice(searched)
        dates= getdates(searched)
        values= price
        Info= information(searched)

        return render_template("search.html",form=form, user=current_user, searched= searched,dates=json.dumps(dates),money=json.dumps(values),Info=Info)
        
@views.route('/data',methods=["GET","POST"])
def data():
    msft = yf.Ticker('msft')
    hist=msft.history(period="3mo")
    price=hist["Open"].tolist()
    prices=json.dumps(price)
    return prices





def getStockPrice(stock):
    msft = yf.Ticker(stock)
    information = yf.download(tickers=stock, period='1d', interval='1m')
    return information['Open'].tolist()

def getdates(stock):
    msft = yf.Ticker(stock)
    information = yf.download(tickers=stock, period='1d', interval='1m')
    dates=[]
    for i in information.index:
        dates.append(i.strftime('%Y-%m-%d %X'))
    
    return dates

def information(stock):
    msft = yf.Ticker(stock)
    return msft.info
