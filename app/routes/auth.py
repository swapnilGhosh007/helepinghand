from ..controllers.auth_controller import AuthController
from flask import Blueprint


auth = Blueprint("auth", __name__, template_folder="../views")
controller = AuthController()


auth.route("/login", methods=["GET", "POST"])(controller.login)
auth.route("/register", methods=["GET", "POST"])(controller.register)
auth.route("/update_password", methods=["GET", "POST"])(controller.update_password)
auth.route("/logout", methods=["GET"])(controller.logout)

