import os
import secrets
from SH import app, db, bcrypt
from PIL import Image
from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
from SH.forms import LoginForm, RegisterForm,MailBoxText
from SH.models import User,  Conversation, Email
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



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form= RegisterForm(request.form)
    if form.validate_on_submit():
        #if current_user.is_authenticated:
        #    return redirect(url_for('home'))
        pw = (form.password.data)
        s = 0
        for char in pw:
            a = ord(char) #ASCII
            s = s+a #sum of ASCIIs acts as the salt
        hashed_password = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
            #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User( email= form.email.data , password= hashed_password, type= form.type.data )
        db.session.add(user)
        db.session.commit()
        flash(f'Success! Please fill in the remaining details', 'success')
        return redirect(url_for('login'))
    return render_template('regForm.html', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        from trained_model2 import classified, SpamClassifier
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
            emails= Email.query.filter_by(user_id=current_user.id).all()
            classification
            for email in emails:
                a=classified(email.received)
                if a ==True:
                    email.spam = email.received
                    db.session.commit()
                else:
                    email.ham = email.received
                    db.session.commit()
                email.received.pop()
                print(a)
            return redirect(next_page) if next_page else redirect(url_for('account'))

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
    email = Email.query.filter_by(user_id=current_user.id).all()
    for message in email:
        messages.append(message.ham)
    return render_template('startpage.html', title='Account',messages= message)

@app.route("/compose", methods= ['POST', 'GET'])
@login_required
def compose():
    form =MailBoxText(request.form)
    if form.validate_on_submit() :
        user_recepient = User.query.filter_by(email = form.recepient.data)
        conversation= Conversation(text = form.text.data, sender_id= current_user.id, receiver_id= user_recepient.id  )
        db.session.add(conversation)
        db.session.commit()
        email = Email(user_id = user_recepient.id, received = conversation.text )
        db.session.add(email)
        db.session.commit()
    return render_template('compose.html', title='Compose', form=form)


@app.route("/spam", methods= ['POST', 'GET'])
@login_required
def spam():
    email = Email.query.filter_by(user_id=current_user.id).all()
    for message in email:
        messages.append(message.ham)
        return render_template('spam.html', title='Account',sponsor_logo=sponsor_logo, form=form)
