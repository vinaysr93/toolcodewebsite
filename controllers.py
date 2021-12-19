from flask import Flask, url_for,send_file
from flask import render_template, request, redirect
from flask import current_app as app
from models import Tool, Standard, User, End_list
from database import db
import requests
import os,random
import csv
import uuid

numl=[]

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message='')

    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        pwd2 = request.form.get("pwd2")
        query_email = User.query.filter_by(useremail=email).all()
        if query_email:

            return render_template("register.html", message="Email already registered   ")
        else:
            if pwd == pwd2:  # Checks if the password is the same
                user_entry = User(useremail=email, userpass=pwd)
                db.session.add(user_entry)
                db.session.commit()
                return render_template("login.html", message='')
            else:
                return render_template("register.html", message="Password doesn't match")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", message='')

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("pwd")
        data_email = User.query.filter_by(useremail=email).first()

        if data_email:
            if data_email.useremail == email:
                data_password = User.query.filter_by(useremail=email).first()

                if password == data_password.userpass:
                    return redirect(url_for("dashboard"))
                else:

                    return render_template("login.html", message="Wrong Password")
            else:

                return render_template("login.html", message="Email Doesn't exist")
        else:

            return render_template("login.html", message="Email doesn't exists")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if request.method == "POST" and "login" in request.form:
        print(request.form)
        item = End_list.query.all()

        if item == []:

            return render_template("dashboard.html", message='No tools are present Add them', item=item)

        else:

            return render_template("dashboard.html",message='',item=item)


    elif request.method == "POST" and 'Add' in request.form:  # Takes care of addition into database

        sk = request.form.get('SK')
        punches = request.form.get('Punches')
        height = request.form.get("height")
        length = request.form.get("length")
        temp_length = length.strip('E')
        quantity = request.form.get("quantity")
        total_quantity = int(temp_length) * int(quantity)

        tool_type_c = Tool.query.filter_by(tool_type=punches, tool_height=height).first()
        tcode = tool_type_c.srnum

        query_code = Standard.query.filter_by(height=height, length=length, tool_type_code=tcode).first()
        catalog_code = query_code.code
        description=query_code.description
        add_entry = End_list(sk=sk, quantity=quantity, length=length, toolcode=catalog_code,description=description)
        db.session.add(add_entry)
        db.session.commit()


        item = End_list.query.all()

        if item == []:

            return render_template("dashboard.html", message='No tools are present Add them', item=item)

        else:

            return render_template("dashboard.html", message='', item=item)


    elif request.method == "GET":

        item = End_list.query.all()

        if item==[]:

            return render_template("dashboard.html", message='No Tools are present', item=item)

        else:
            return render_template("dashboard.html",message='', item=item)

    elif request.method == "POST" and 'Update' in request.form:  # Takes care of updation into database

        sk = request.form.get('SK')
        punches = request.form.get('Punches')
        height = request.form.get("height")
        length = request.form.get("length")
        temp_length = length.strip('E')
        quantity = request.form.get("quantity")
        total_quantity = int(temp_length) * int(quantity)
        srnum=int(numl[-1])

        tool_type_c = Tool.query.filter_by(tool_type=punches, tool_height=height).first()
        tcode = tool_type_c.srnum

        query_code = Standard.query.filter_by(height=height, length=length, tool_type_code=tcode).first()
        catalog_code = query_code.code
        description = query_code.description


        update_entry=End_list.query.filter_by(srnuml=srnum).first()
        update_entry.sk=sk
        update_entry.quantity=int(quantity)
        update_entry.length=length
        update_entry.toolcode=catalog_code
        update_entry.description=description
        db.session.commit()

        item = End_list.query.all()
        return render_template("dashboard.html", message='', item=item)

@app.route("/delete/<srnum>", methods=["GET", "POST"])
def delete_entry(srnum):

    del_entry = End_list.query.filter_by(srnuml=srnum).first()
    db.session.delete(del_entry)
    db.session.commit()

    return redirect("/dashboard")

@app.route("/tool_individual_punch", methods=["GET", "POST"])
def tool_individual_punch():
    if request.method == "GET":
        return render_template("tool_individual.html")

    if request.method == "POST":
        pass

@app.route("/tool_individual_die",methods=["GET","POST"])
def tool_individual_die():
    if request.method=="GET":
        return redirect(url_for("dashboard"))


@app.route("/update/<num>")
def update(num):
    if request.method=="GET":

        numl.append(num)

        query_call=End_list.query.filter_by(srnuml=num).first()
        sk=query_call.sk
        code=query_call.toolcode
        description=query_call.description.split()
        punch=description[0]
        if "90" in description:
            query_height=90
        else:
            query_height=120
        length=query_call.length

        print(sk,punch,length,query_height)
        return render_template("update.html",sk=sk,punch=punch,height=query_height,length=length)


@app.route("/export_file",methods=["GET","POST"])
def export_file():


    if request.method=='GET':

        export_list=End_list.query.all()
        print(export_list)
        filename = str(uuid.uuid4())
        outfile = open(f'{filename}.csv', 'w',newline='')
        outcsv = csv.writer(outfile)
        outcsv.writerow(["Sr Number","SK","Quantity","Length","ToolCode","Description"])
        for x in export_list:

             outcsv.writerow([x.srnuml,x.sk,x.quantity,x.length,x.toolcode,x.description.strip()])

        outfile.close()
        return url_for("dashboard")


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
