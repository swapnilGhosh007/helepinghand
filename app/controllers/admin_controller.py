from flask import render_template, redirect, url_for, request, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from ..models.models import User, BasicUser, Client, Worker, Feedback
from ..extensions import db


class AdminController:
    
    def view_users(self):
        users = BasicUser.query.all()
        return render_template("user_list.html", users = users)
    def view_clients(self):
        users = Client.query.all()
        return render_template("user_list.html", users = users)
    def view_workers(self):
        users = Worker.query.all()
        return render_template("worker_list.html", users = users)
    def ban_user(self,id):
        user = BasicUser.query.get(id)
        user.ban = True
        db.session.commit()
        return redirect(url_for("admin.view_users"))
    
    def approve_worker(self, id):
        if request.method == "POST":
            user = Worker.query.get(id)
            user.hourly_rate = request.form.get("hourly_rate")
            user.approval = True
            db.session.commit()
            return redirect(url_for("admin.view_users"))
        return render_template("approve_worker.html")