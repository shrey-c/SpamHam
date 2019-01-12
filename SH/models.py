from SH import db, login_manager
from flask_login import UserMixin
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(120), unique=True)
    password= db.Column(db.String(150), nullable=False)
    conversing = db.relationship("Conversing", back_populates ="user")

    def __repr__(self):
        return f"User('{self.email}')"

class Conversing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    user = db.relationship("User", back_populates ="conversing")
    user2 = db.Column(db.Integer)
    conversation=db.relationship("Conversation", uselist=False, back_populates ="conversing")
    def __repr__(self):
        return f"Conversing('{self.user1}','{self.user2}')"

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    conversing_id = db.Column(db.Integer, db.ForeignKey('conversing.id'))
    conversing= db.relationship("Conversing", uselist=False, back_populates ="conversation" )
    sender_id = db.Column(db.Integer, unique = False , nullable= False )
    def __repr__(self):
        return f"Conversation('{self.text}','{self.time}','{self.conversing_id}', '{self.sender_id}')"
