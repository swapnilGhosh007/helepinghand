from ..controllers.client_controller import ClientController
from flask import Blueprint


client = Blueprint("client", __name__, template_folder="../views")
controller = ClientController()

client.route("/submit_review/<id>", methods=["GET", "POST"])(controller.submit_review)
client.route("/search_worker", methods=["GET", "POST"])(controller.search_worker)
client.route("/worker/<id>", methods=["GET"])(controller.view_worker)
client.route("/book_worker/<id>", methods=["GET", "POST"])(controller.book_worker)
client.route("/payment/<id>", methods=["GET", "POST"])(controller.payment)
client.route("/my_workers", methods=["GET"])(controller.view_past_workers)
