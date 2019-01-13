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
#from googlemaps import Client as GoogleMaps
import requests
from sqlalchemy import or_ , and_
import pickle


loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
print(loaded_model)


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
    return render_template('selectForm.html', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

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
        ##

        return render_template('account.html', title='Account',sponsor_logo=sponsor_logo, form=form)

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

        return render_template('compose.html', title='Account',sponsor_logo=sponsor_logo, form=form)

@app.route("/received", methods= ['POST', 'GET'])
@login_required
def account():

        return render_template('received.html', title='Account',sponsor_logo=sponsor_logo, form=form)

@app.route("/spam", methods= ['POST', 'GET'])
@login_required
def account():

        return render_template('spam.html', title='Account',sponsor_logo=sponsor_logo, form=form)

@app.route("/sent", methods= ['POST', 'GET'])
@login_required
def account():

        return render_template('sent.html', title='Account',sponsor_logo=sponsor_logo, form=form)

@app.route("/user/<user2_id>", methods = ['GET', 'POST'])
@login_required
def user2_account(user2_id):

    conversing=Conversing.query.filter(and_(Conversing.user1==current_user.id,Conversing.user2==user2_id)).first()
    if conversing==None:

        if current_user.type == 'P':

            form=InviteForm()
            sponsorUser=SponsorUser.query.filter_by(user_id=user2_id).first()
            flag=1
            if form.validate_on_submit():
                conversing=Conversing(user1=current_user.id,user2=user2_id,status='Sent')
                db.session.add(conversing)
                db.session.commit()

            return render_template('User2Account_sponsor.html', title='Account', sponsorUser=sponsorUser, current_user=current_user,form=form,flag=flag)

        elif current_user.type == 'S':

            form=InviteForm()
            partyUser = PartyUser.query.filter_by(user_id=user2_id).first()
            flag=1
            if form.validate_on_submit():
                conversing=Conversing(user1=current_user.id,user2=user2_id,status='Sent')
                db.session.add(conversing)
                db.session.commit()

            return render_template('User2Account_party.html', title='Account', partyUser=partyUser, current_user=current_user,form=form,flag=flag)

    else:
        if current_user.type == 'P':
            flag=0
            sponsorUser=SponsorUser.query.filter_by(user_id=user2_id).first()
            db.session.commit()
            return render_template('User2Account_sponsor.html', title='Account', sponsorUser=sponsorUser, current_user=current_user,flag=flag)

        elif current_user.type == 'S':
            flag=0
            partyUser = PartyUser.query.filter_by(user_id=user2_id).first()
            db.session.commit()
            return render_template('User2Account_party.html', title='Account', partyUser=partyUser, current_user=current_user,flag=flag)


@app.route("/chatwith", methods= ['POST', 'GET'])#Whom do you want to chat with?
@login_required
def chatwith():
    associated_users_list=[]
    conversing= Conversing.query.filter(or_(Conversing.user1==current_user.id,Conversing.user2==current_user.id)).all()
    conversing2= Conversing.query.filter(or_(Conversing.user1==current_user.id,Conversing.user2==current_user.id)).first()


    if conversing2 == None:
        print('10001')
        return render_template ('chatError.html', title = 'Chat Error',current_user=current_user)
    else:
        for nowuser in conversing :
            print('1000')
            print(nowuser.status)
            if nowuser.user1== current_user.id:
                if nowuser.status=='In-touch':
                    if current_user.type == 'P':
                        sponsorUser= SponsorUser.query.filter_by(user_id=nowuser.user2).first()
                        associated_user=[sponsorUser.user_id,sponsorUser.sponsor_name]
                        associated_users_list.append(associated_user)
                    elif current_user.type == 'S':
                        partyUser= PartyUser.query.filter_by(user_id=nowuser.user2).first()
                        associated_user=[partyUser.user_id,partyUser.party_name]
                        associated_users_list.append(associated_user)
            elif nowuser.user2== current_user.id:
                if nowuser.status=='In-touch':
                    if current_user.type == 'P':
                        sponsorUser= SponsorUser.query.filter_by(user_id=nowuser.user1).first()
                        associated_user=[sponsorUser.user_id,sponsorUser.sponsor_name]
                        associated_users_list.append(associated_user)
                    elif current_user.type == 'S':
                        partyUser= PartyUser.query.filter_by(user_id=nowuser.user1).first()
                        associated_user=[partyUser.user_id,partyUser.party_name]
                        associated_users_list.append(associated_user)
        if associated_users_list==[]:
            return render_template ('chatError.html', title = 'No Users')
        return render_template ('chatlist.html', title = 'Chat with', associated_users_list=associated_users_list)



    #return associated_users_choices
@app.route("/chatbox/<chatwith_id>", methods= ['POST', 'GET'])#Whom do you want to chat with?
@login_required
def chat(chatwith_id):
    print(chatwith_id)
    form=MailBoxText()
    messages=[]
    conversing= Conversing.query.filter(or_(Conversing.user1==chatwith_id,Conversing.user2==chatwith_id)).all()
    for nowuser in conversing:
        if current_user.type=='P':
            if nowuser.user1== current_user.id:

                user=SponsorUser.query.filter_by(user_id=nowuser.user2).first()
                messages=[[user.sponsor_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id  )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                    message=[conversation.text,conversation.time, conversation.sender_id]
                    messages.append(message)

            elif  nowuser.user2==current_user.id:
                user=User.query.filter_by(user_id=nowuser.user2).first()
                messages=[[user.sponsor_name]]
                if form.validate_on_submit() :
                    conversation= Conversation(text = form.text.data, conversing_id= nowuser.id, sender_id= current_user.id  )
                    db.session.add(conversation)
                    db.session.commit()
                for conversation in Conversation.query.filter_by(conversing_id = nowuser.id).all():
                    message=[conversation.text,conversation.time, conversation.sender_id]#just for now
                    messages.append(message)

    return render_template('chatbox.html', title= 'ChatBox', form=form, messages=messages, current_user=current_user, user=user)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/MeetTheTeam")
def team():
    return render_template('MeetTheTeam.html')


@app.route("/WhatWeDo")
def work():
    return render_template('WhatWeDo.html')


@app.route('/email', methods = ['GET', 'POST'])
@login_required
def email():
    return render_template('email.html', title='Email')
