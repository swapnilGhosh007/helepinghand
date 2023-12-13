from flask import render_template, redirect, url_for, request, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from ..models.models import User, BasicUser, Client, Worker, Feedback
from ..extensions import db


class AdminController:
    @login_required
    def view_users(self):
        if current_user.user_type != "admin":
            return redirect(url_for("user.profile"))
        users = BasicUser.query.all()
        return render_template("user_list.html", users = users)
    @login_required
    def view_clients(self):
        if current_user.user_type != "admin":
            return redirect(url_for("user.profile"))
        users = Client.query.all()
        return render_template("user_list.html", users = users)
    @login_required
    def view_workers(self):
        if current_user.user_type != "admin":
            return redirect(url_for("user.profile"))
        users = Worker.query.all()
        return render_template("worker_list.html", users = users)
    @login_required
    def ban_user(self,id):
        if current_user.user_type != "admin":
            return redirect(url_for("user.profile"))
        user = BasicUser.query.get(id)
        user.ban = True
        db.session.commit()
        return redirect(url_for("admin.view_users"))
    @login_required
    def approve_worker(self, id):
        if current_user.user_type != "admin":
            return redirect(url_for("user.profile"))
        if request.method == "POST":
            user = Worker.query.get(id)
            user.hourly_rate = request.form.get("hourly_rate")
            user.approval = True
            db.session.commit()
            return redirect(url_for("admin.view_users"))
        return render_template("approve_worker.html")