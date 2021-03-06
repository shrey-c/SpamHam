from SH import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email_id= db.Column(db.String(120))
    password= db.Column(db.String(150), nullable=False)
    email = db.relationship("Emails", back_populates ="user")
    received = db.Column(db.String(1500), nullable=True)
    spam = db.Column(db.String(1500), nullable=True)
    ham = db.Column(db.String(1500), nullable=True)
    def __repr__(self):
        return f"User('{self.email_id}','{self.received}','{self.spam}','{self.ham}')"

#class Conversing(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #user1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    #user = db.relationship("User", back_populates ="conversing")
    #user2 = db.Column(db.Integer)
    #conversation=db.relationship("Conversation", uselist=False, back_populates ="conversing")
    #def __repr__(self):
        #return f"Conversing('{self.user1}','{self.user2}')"

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1500), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #conversing_id = db.Column(db.Integer, db.ForeignKey('conversing.id'))
    #conversing= db.relationship("Conversing", uselist=False, back_populates ="conversation" )
    sender_id = db.Column(db.Integer, unique = False , nullable= False )
    receiver_id = db.Column(db.Integer, unique = False , nullable= False )
    def __repr__(self):
        return f"Conversation('{self.text}','{self.time}','{self.conversing_id}', '{self.sender_id}')"


class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", back_populates ="email")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    received = db.Column(db.String(1500), nullable=True)
    spam = db.Column(db.String(1500), nullable=True)
    ham = db.Column(db.String(1500), nullable=True)
    def __repr__(self):
        return f"Email('{self.user_id}','{self.received}','{self.spam}','{self.ham}')"
