from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import stripe
import os


db = SQLAlchemy()


migrate = Migrate()


stripe_keys = {
    "public_key": os.environ.get("STRIPE_PUBLIC_KEY"),
    "stripe_api_key": os.environ.get("STRIPE_API_KEY"),
}

stripe.api_key = stripe_keys["stripe_api_key"]


login_manager = LoginManager()
login_manager.login_view = "auth.login"


def init_user_loader(UserClass):
    @login_manager.user_loader
    def load_user(id):
        return UserClass.query.get(id)
