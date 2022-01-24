#store the standard route to the website
from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash, jsonify
from flask_login import  login_required, current_user
from .models import Stock
from .  import db
import json

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home(): #this function will run everytime we access the view's route
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
    return  render_template("home.html", user=current_user)# return the html file that we want to render to the website


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



