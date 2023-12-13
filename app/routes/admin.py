from ..controllers.admin_controller import AdminController
from flask import Blueprint


admin = Blueprint("admin", __name__, template_folder="../views")
controller = AdminController()


admin.route("/view_users",methods=["GET"])(controller.view_users)
admin.route("/view_clients",methods=["GET"])(controller.view_clients)
admin.route("/view_workers",methods=["GET"])(controller.view_workers)
admin.route("/ban_user/<id>",methods=["GET"])(controller.ban_user)
admin.route("/approve_worker/<id>",methods=["GET","POST"])(controller.approve_worker)


