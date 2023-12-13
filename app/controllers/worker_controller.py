from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from ..models.models import User, BasicUser, Client, Worker, Review, Schedule
from ..extensions import db


class WorkerController:
    
    @login_required
    def view_reviews(self):
        if current_user.user_type != "worker":
            return redirect(url_for("user.profile"))
        reviews = Review.query.filter_by(worker_id=current_user.id).all()

        return render_template("view_reviews.html", reviews=reviews)
    @login_required
    def update_schedule(self):
        if current_user.user_type != "worker":
            return redirect(url_for("user.profile"))
        schedule = Schedule.query.filter_by(worker_id=current_user.id).first()
        if request.method == "POST":
            slot1 = True if request.form.get("slot1") == "on" else False
            slot2 = True if request.form.get("slot2") == "on" else False
            slot3 = True if request.form.get("slot3") == "on" else False
            slot4 = True if request.form.get("slot4") == "on" else False
            if schedule:
                schedule.slot1 = slot1
                schedule.slot2 = slot2
                schedule.slot3 = slot3
                schedule.slot4 = slot4
            else:
                schedule = Schedule(
                    worker_id=current_user.id,
                    slot1=slot1,
                    slot2=slot2,
                    slot3=slot3,
                    slot4=slot4,
                )

                db.session.add(schedule)
            db.session.commit()

            return redirect(url_for("user.profile"))
        return render_template("update_schedule.html", schedule=schedule)
    @login_required
    def update_cv(self):
        if current_user.user_type != "worker":
            return redirect(url_for("user.profile"))
        if request.method == "POST":
            occupation = request.form.get("occupation")
            experience = request.form.get("experience")
            marital_status = request.form.get("marital_status")

            worker = Worker.query.get(current_user.id)

            worker.occupation = occupation
            worker.initial_experience = experience
            if marital_status == "1":
                worker.marital_status = True
            else:
                worker.marital_status = False

            db.session.commit()

            return redirect(url_for("user.profile"))

        return render_template("update_cv.html")
