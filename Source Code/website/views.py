#store the standard route to the website
from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash, jsonify
from flask_login import  login_required, current_user
from .models import Stock
from . import db
from .searchform import SearchForm
from .stockview import getData
import json
from flask_mail import Mail, Message
from . import mail

views = Blueprint('views',__name__)

#home page
@views.route('/', methods=['GET','POST'])
def home():
    return  render_template("home.html", user=current_user)


#profile
@views.route('/profile', methods=['GET','POST'])
@login_required
def profile(): #this function will run everytime we access the view's route
    if(request.method == "POST"):
        stock = request.form.get('stock')

        if(Stock.query.filter_by(name = stock).first()):
            flash(stock + " is already existed in your stock list", category = "error")

        elif (len(stock)<0):
            flash("stock name is too short!", category = "error")

        else:

            new_stock = Stock(name = stock, user_id = current_user.id)
            db.session.add(new_stock)
            db.session.commit()
            flash("new Stock added!", category = "success")
    return  render_template("profile.html", user=current_user)# return the html file that we want to render to the website


# delete stock name
@views.route('delete-stock', methods=['POST'])
def delete_stock():
    stock = json.loads(request.data)
    stockId = stock['stockId']
    stock =Stock.query.get(stockId)
    if (stock):
        if (stock.user_id == current_user.id):
            flash(stock.name+ "is successfully removed")
            db.session.delete(stock)
            db.session.commit()
            
    return jsonify({})

#send message
@views.route('/contactus',methods=['GET','POST'])
def message():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        message=request.form.get('message')
        msg= Message(subject=f'Mail from {name}', body=f'{message}', sender = email, recipients = ['ropofo6438@yks247.com'])
        mail.send(msg)
        flash("Thank you for contact us.",category = "success")
        flash("Your message was sent. We will contact you soon.",category = "success")
    return render_template("contactus.html", user=current_user)

#Pass stuff to Navbar
@views.context_processor
def base():
    form = SearchForm()
    return dict(form = form)

#search
@views.route('/search', methods=["POST"])
def search():
    form =SearchForm()
    if (form.validate_on_submit()):
        searched = form.search.data
        print(getData(searched))
        return render_template("search.html",form=form, user=current_user, searched= searched)





