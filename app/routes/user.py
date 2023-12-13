from ..controllers.user_controller import UserController
from flask import Blueprint

user = Blueprint("user", __name__, template_folder="../views")
controller = UserController()

user.route("/profile", methods=["GET"])(controller.profile)
user.route("/update_profile", methods=["GET", "POST"])(controller.update_profile)
user.route("/submit_feedback", methods=["GET", "POST"])(controller.submit_feedback)
