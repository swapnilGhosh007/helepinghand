from ..controllers.worker_controller import WorkerController
from flask import Blueprint


worker = Blueprint("worker", __name__, template_folder="../views")
controller = WorkerController()

worker.route("/view_reviews", methods=["GET"])(controller.view_reviews)
worker.route("/update_schedule", methods=["GET", "POST"])(controller.update_schedule)
worker.route("/update_cv", methods=["GET", "POST"])(controller.update_cv)