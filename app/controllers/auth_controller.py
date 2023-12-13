from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from ..models.models import User, Client, Worker
from datetime import datetime
from ..extensions import db


class AuthController:
    def login(self):
        if request.method == "POST":
            if current_user.is_authenticated:
                return redirect(url_for("home"))

            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter_by(username=username).first()

            if user is None:
                flash("Username not found", "error")
                return redirect(url_for("auth.login"))
            elif user.user_type!="admin" and user.ban:
                flash("You are banned", "error")
                return redirect(url_for("auth.login"))
            elif user.match_password(password):

                login_user(user, remember=True)
                flash("Logged in successfully!", "success")
                if user.user_type == 'admin':
                    return redirect(url_for("admin.view_users"))
                return redirect(url_for("user.profile"))

            else:
                flash("Wrong Password", "error")
                return redirect(url_for("auth.login"))

        return render_template("login.html")

    def register(self):
        if current_user.is_authenticated:
            return redirect(url_for("user.profile", username=current_user.username))

        if request.method == "POST":
            name = request.form.get("name")
            username = request.form.get("username")
            email = request.form.get("email")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            user_type = request.form.get("user_type")

            if password1 != password2:
                flash("Passwords do not match", "error")
                return redirect(url_for("auth.register"))

            if User.query.filter_by(username=username).first():
                flash("Username already exists", "error")
                return redirect(url_for("auth.register"))

            if User.query.filter_by(email=email).first():
                flash("Email already exists", "error")
                return redirect(url_for("auth.register"))

            if password1 != password2:
                flash("Passwords do not match", "error")
                return redirect(url_for("auth.register"))

            if len(password1) < 4:
                flash("Password must be at least 4 characters", "error")
                return redirect(url_for("auth.register"))

            if user_type == "client":
                user = Client(
                    fullname=name,
                    username=username,
                    email=email,
                    password=password1,
                )
            elif user_type == "worker":
                user = Worker(
                    fullname=name,
                    username=username,
                    email=email,
                    password=password1,
                    join_date=datetime.now(),
                )

            db.session.add(user)

            db.session.commit()

            login_user(user, remember=True)

            # flash("Account created successfully!", "success")

            return redirect(url_for("user.profile"))

        return render_template("register.html")

    @login_required
    def update_password(self):
        if request.method == "POST":
            old_password = request.form.get("old_password")

            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            if password1 != password2:
                # flash("Passwords do not match", "error")
                return redirect(url_for("auth.update_password"))

            if not current_user.match_password(old_password):
                # flash("Old password is incorrect", "error")
                return redirect(url_for("auth.update_password"))

            if len(password1) < 4:
                # flash("Password must be at least 4 characters", "error")
                return redirect(url_for("auth.register"))

            current_user.password = password1

            db.session.commit()

            return redirect(url_for("user.profile"))

        return render_template("update_password.html")

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for("auth.login"))
