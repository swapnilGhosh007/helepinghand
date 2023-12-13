from flask import render_template, redirect, url_for, request, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from ..models.models import User, BasicUser, Client, Worker, Feedback
from ..extensions import db


class UserController:
    @login_required
    def profile(self):
        user = current_user
        if user.user_type == "client":
            user = Client.query.get(user.id)

        elif user.user_type == "worker":
            user = Worker.query.get(user.id)

        return render_template("profile.html", user=user)

    @login_required
    def update_profile(self):
        # if current_user.id != id:
        #     return redirect(url_for("user.profile"))
        user = BasicUser.query.get(current_user.id)
        if request.method == "POST":
            

            name = request.form.get("name")
            username = request.form.get("username")
            email = request.form.get("email")
            nid = request.form.get("nid")
            phone = request.form.get("phone")
            address = request.form.get("address")

            user.fullname = name

            user.address = address

            user.phone = phone

            existing_user_by_username = BasicUser.query.filter_by(username=username).first()
            
            if existing_user_by_username and existing_user_by_username.id != current_user.id:
                flash("Username already exists", "error")
                return redirect(url_for("user.update_profile"))

            user.username = username

            if len(BasicUser.query.filter_by(email=email).all()) >= 2:
                # flash("Email already exists", "error")
                return redirect(url_for("user.update_profile"))

            user.email = email

            existing_user_by_nid = BasicUser.query.filter_by(nid=nid).first()
            if existing_user_by_nid and existing_user_by_nid.id != current_user.id:
                flash("NID belongs to another person!", "error")
                return redirect(url_for("user.update_profile"))

            user.nid = nid

            db.session.commit()

            return redirect(url_for("user.profile"))

        return render_template("update_profile.html", user=user)

    @login_required
    def submit_feedback(self):
        if request.method == "POST":
            comment = request.form.get("comment")

            feedback = Feedback(comment=comment, user_id=current_user.id)

            db.session.add(feedback)
            db.session.commit()

            return redirect(url_for("user.profile"))

        return render_template("submit_feedback.html")
