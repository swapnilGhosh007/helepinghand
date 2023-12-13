from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    user_type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "base_user",
        "polymorphic_on": "user_type",
    }

    @property
    def password(self):
        return AttributeError("Write-Only Field")

    @password.setter
    def password(self, passwrd):
        self._password = generate_password_hash(passwrd)

    def match_password(self, passwrd):
        return check_password_hash(self._password, passwrd)


class Admin(User):
    __tablename__ = "admins"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "admin"}


class BasicUser(User):
    __tablename__ = "basic_users"
    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    nid = db.Column(db.String(50), unique=True, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    ban=db.Column(db.Boolean , default=False)
    __mapper_args__ = {"polymorphic_identity": "basic_user"}



class Client(BasicUser):
    __tablename__ = "clients"
    id = db.Column(db.Integer, db.ForeignKey("basic_users.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "client"}


class Worker(BasicUser):
    __tablename__ = "workers"
    id = db.Column(db.Integer, db.ForeignKey("basic_users.id"), primary_key=True)
    join_date = db.Column(db.DateTime, nullable=False)
    occupation = db.Column(db.String(50), nullable=True)
    initial_experience = db.Column(db.Integer, nullable=True)
    marital_status = db.Column(db.Boolean, nullable=True)
    hourly_rate = db.Column(db.Integer, nullable=True)
    approval = db.Column(db.Boolean, default=False)
    __mapper_args__ = {"polymorphic_identity": "worker"}

    def get_deals(self):
        return ClientWorkerDeal.query.filter_by(worker_id=self.id).all()

    def get_experience(self):
        current_year = datetime.now().year
        year = self.join_date.year
        return self.initial_experience + (current_year - year)

    def get_rating(self):
        
        reviews = Review.query.filter_by(worker_id=self.id).all()
        if len(reviews) == 0:
            return 'No reviews yet'
        rating = 0
        for review in reviews:
            rating += review.rating
        return rating / len(reviews)


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(200), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey("workers.id"), nullable=False)


class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    worker_id = db.Column(db.Integer, db.ForeignKey("workers.id"), nullable=False)
    slot1 = db.Column(db.Boolean, nullable=False)
    slot2 = db.Column(db.Boolean, nullable=False)
    slot3 = db.Column(db.Boolean, nullable=False)
    slot4 = db.Column(db.Boolean, nullable=False)


class ClientWorkerDeal(db.Model):
    __tablename__ = "client_worker_deals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey("workers.id"), nullable=False)
    slot1 = db.Column(db.Boolean, nullable=False)
    slot2 = db.Column(db.Boolean, nullable=False)
    slot3 = db.Column(db.Boolean, nullable=False)
    slot4 = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_worker_deal_id = db.Column(
        db.Integer, db.ForeignKey("client_worker_deals.id"), nullable=False
    )
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Feedback(db.Model):
    __tablename__ = "feedbacks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comment = db.Column(db.String(200), nullable=False)
