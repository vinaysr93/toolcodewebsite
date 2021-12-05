from flask import Flask
from flask import render_template, request, redirect
from flask import current_app as app
from models import Tool,Standard,User
from database import db
import requests

@app.route("/register",methods=["GET","POST"])
def register():


    if request.method=="GET":

        return render_template("register.html",message='')

    if request.method=="POST":
        email=request.form.get("email")
        pwd=request.form.get("pwd")
        pwd2=request.form.get("pwd2")
        query_email=User.query.filter_by(useremail=email).all()
        if query_email:

            return render_template("register.html", message="Email already registered   ")
        else:
            if pwd == pwd2:  # Checks if the password is the same
                user_entry = User(useremail=email,userpass=pwd)
                db.session.add(user_entry)
                db.session.commit()
                return render_template("login.html",message='')
            else:
                return render_template("register.html", message="Password doesn't match")

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method=="GET":
        return render_template("login.html",message='')

    if request.method=="POST":

        email= request.form.get("email")
        password= request.form.get("pwd")
        data_email=User.query.filter_by(useremail=email).first()



        if data_email:
            if data_email.useremail==email:
                data_password=User.query.filter_by(useremail=email).first()
                print(data_password.userpass)
                if password==data_password.userpass:
                    return render_template("dashboard.html")
                else:

                    return render_template("login.html",message="Wrong Password")
            else:

                return render_template("login.html",message="Email Doesn't exist")
        else:

            return render_template("login.html",message="Email doesn't exists")

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():

    return render_template("dashboard.html")
# @app.route("/dashboard/<user_name>", methods=["GET", "POST"])
# def dashboard(user_name):
#     user_id = User.query.filter_by(user_cred=user_name).first().user_id
#     print(user_id)
#     decks = Decks.query.filter_by(deck_user_id=user_id).all()
#     dl = len(decks)
#
#     return render_template("dashboard.html", decks=decks, ld=dl, user_name=user_name)
#
#     pass
#
#
# @app.route("/dashboard/<user_name>/adddeck", methods=["GET", "POST"])
# def adddeck(user_name):
#     user_id = User.query.filter_by(user_cred=user_name).first().user_id
#
#     if request.method == "GET":
#         return render_template("adddeck.html",user_name=user_name)
#
#     elif request.method=="POST":
#
#         deck_name=request.form.get("deck_name")
#         deck_description=request.form.get("deck_description")
#
#         add_entry=Decks(deck_user_id=user_id,deck_name=deck_name,deck_description=deck_description)
#         db.session.add(add_entry)
#         db.session.commit()
#
#         return redirect("/dashboard/<user_name>",user_name=user_name)
#
# @app.route("/deck/<user_name>/<deck_id>/update", methods=["GET", "POST"])
# def deck_update(user_name,deck_id):
#
#     user_name=user_name
#
#     return render_template("update.html")
#
# @app.route("/deck/<user_name>/<deck_id>/delete", methods=["GET", "POST"])
# def deck_delete(user_name, deck_id):
#     k = User.query.filter_by(user_cred=user_name).first().user_id
#
#
#     Decks.query.filter_by(id=deck_id,deck_user_id=k).delete()
#     db.session.commit()
#     return redirect("/dashboard/<user_name>",user_name=user_name)