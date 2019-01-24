import os
import secrets
from SH import app, db, bcrypt
from PIL import Image
from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
from SH.forms import LoginForm, RegisterForm, MailBoxText
from SH.models import User, Conversation, Emails
import hashlib #for SHA512
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import Session
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from math import log, sqrt
import pandas as pd
import numpy as np
import re
from sklearn.externals import joblib
import requests
from sqlalchemy import or_ , and_
from SH.trained_model2 import classified, SpamClassifier
import SH.trained_model2


@app.route("/")
@app.route("/home")
def home():
    return render_template('startpage.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form= RegisterForm(request.form)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        pw = (form.password.data)
        s = 0
        for char in pw:
            a = ord(char) #ASCII
            s = s+a #sum of ASCIIs acts as the salt
        hashed_password = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
            #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User( email_id= form.email_id.data , password= hashed_password )
        db.session.add(user)
        db.session.commit()
        flash(f'Success! Please fill in the remaining details', 'success')
        return redirect(url_for('login'))
    return render_template('regForm.html', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email_id=form.email_id.data).first()

        #modified to use SHA512

        s = 0
        for char in (form.password.data):
            a = ord(char)
            s = s+a
        now_hash = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
        #if user and bcrypt.check_password_hash(user.password, form.password.data):
        if (user and (user.password==now_hash)):

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            ##ML PART
            emails= Emails.query.filter_by(user_id=current_user.id).all()

            for email in emails:
                if email.spam or email.ham:
                    continue
                else:
                    a=classified(email.received)
                    if a ==True:
                        email.spam = email.received
                        db.session.commit()
                    else:
                        email.ham = email.received
                        db.session.commit()
                    print(a)
            print(emails)
            return redirect(url_for('account'))
        else:
            print('halaaa2')
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print('halaaa2')
    else:
        print('halaaa1')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods= ['POST', 'GET'])
@login_required
def account():
    messages=[]
    message = ''
    email = Emails.query.filter_by(user_id=current_user.id).all()
    print(email)
    for message in email:
        if message.ham != None :
            conversation = Conversation.query.filter_by(text=message.ham).first()
            user = User.query.filter_by(id=conversation.sender_id).first()
            messages.append([user.email_id,message.ham,conversation.time])
            print(message)
    return render_template('home.html', title='Account',messages= messages,current_user=current_user)

@app.route("/spam", methods= ['POST', 'GET'])
@login_required
def spam():
    messages=[]
    message = ''
    email = Emails.query.filter_by(user_id=current_user.id).all()
    email_temp = email
    print(email)
    for message in email:
        message_temp = message
        if message.spam != None :
            conversation = Conversation.query.filter_by(text=message.spam).first()
            user = User.query.filter_by(id=conversation.sender_id).first()
            messages.append([user.email_id,message.spam,conversation.time])
            print(message)
    return render_template('spam.html', title='Spam',messages=messages,current_user=current_user)


@app.route("/compose", methods= ['POST', 'GET'])
@login_required
def compose():
    form =MailBoxText(request.form)
    if form.validate_on_submit():
        user_recepient = User.query.filter_by(email_id = form.email_id.data).first()
        if user_recepient == None:
            flash('Receivers email doesnt exist', 'danger')
            return redirect(url_for('account'))
        conversation= Conversation(text = form.text.data, sender_id= current_user.id, receiver_id= user_recepient.id  )
        db.session.add(conversation)
        db.session.commit()
        print('apiu')
        if conversation.sender_id==conversation.receiver_id:
            email = Emails(user_id = user_recepient.id, received = conversation.text, ham = conversation.text )
        else:
            email = Emails(user_id = user_recepient.id, received = conversation.text)
        print('vidho')
        db.session.add(email)
        db.session.commit()
        print(email)
        return redirect(url_for('account'))
    else:
        print('halaaa2')
        flash('Login Unsuccessful. Please check email and password', 'danger')
        print('halaaa2')
    return render_template('compose.html', title='Compose', form=form,current_user=current_user)
