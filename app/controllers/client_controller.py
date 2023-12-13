from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from ..models.models import (
    User,
    BasicUser,
    Client,
    Worker,
    Review,
    ClientWorkerDeal,
    Payment, Schedule,
)
from datetime import datetime
import stripe
from ..extensions import db, stripe_keys


class ClientController:
    @login_required
    def search_worker(self):
        if current_user.user_type != "client":
            return redirect(url_for("user.profile"))
        if request.method == "POST":
            occupation = request.form.get("occupation")
            slot1 = True if request.form.get("slot1") == "on" else False
            slot2 = True if request.form.get("slot2") == "on" else False
            slot3 = True if request.form.get("slot3") == "on" else False
            slot4 = True if request.form.get("slot4") == "on" else False
            print(slot1,slot2,slot3,slot4)

            workers = Worker.query.filter_by(occupation=occupation, approval=True).all()

            results = []

            for worker in workers:
                schedule = Schedule.query.filter_by(worker_id=worker.id).first()
                if schedule is None:
                    continue
                deals = ClientWorkerDeal.query.filter_by(worker_id=worker.id, active=True).all()
                for deal in deals:
                    if schedule.slot1 and deal.slot1:
                        schedule.slot1 = False
                    if schedule.slot2 and deal.slot2:
                        schedule.slot2 = False
                    if schedule.slot3 and deal.slot3:
                        schedule.slot3 = False
                    if schedule.slot4 and deal.slot4:
                        schedule.slot4 = False

                if (slot1 and schedule.slot1) or not slot1:
                    if (slot2 and schedule.slot2) or not slot2:
                        if (slot3 and schedule.slot3) or not slot3:
                            if (slot4 and schedule.slot4) or not slot4:
                                results.append(worker)

            return render_template("search_results.html", results=results)
                
        return render_template("search_worker.html")
    @login_required
    def view_worker(self, id):
        if current_user.user_type != "client":
            return redirect(url_for("user.profile"))
        worker = Worker.query.filter_by(id=id).first()
        if worker is None:
            # flash("Worker not found", "error")
            return redirect(url_for("client.search_worker"))

        return render_template("worker_profile.html", user=worker)
    @login_required
    def view_past_workers(self):
        if current_user.user_type != "client":
            return redirect(url_for("user.profile"))
        deals = ClientWorkerDeal.query.filter_by(client_id=current_user.id).all()
        workers = []
        for deal in deals:
            worker = Worker.query.filter_by(id=deal.worker_id).first()
            workers.append(worker)
        return render_template("my_workers.html", results=workers)
    @login_required
    def book_worker(self, id):
        if current_user.user_type != "client":
            return redirect(url_for("user.profile"))
        worker = Worker.query.filter_by(id=id).first()
        if worker is None:
            flash("Worker not found", "error")
            return redirect(url_for("client.search_worker"))

        schedule = Schedule.query.filter_by(worker_id=worker.id).first()

        if request.method == "POST":
            slot1 = True if request.form.get("slot1") == "on" else False
            slot2 = True if request.form.get("slot2") == "on" else False
            slot3 = True if request.form.get("slot3") == "on" else False
            slot4 = True if request.form.get("slot4") == "on" else False
            
            deal = ClientWorkerDeal(
                client_id=current_user.id,
                worker_id=worker.id,
                slot1=slot1,
                slot2=slot2,
                slot3=slot3,
                slot4=slot4,
                active=False,
            )

            db.session.add(deal)
            db.session.commit()

            return redirect(url_for("client.payment", id=deal.id))
        deals = ClientWorkerDeal.query.filter_by(worker_id=worker.id, active=True).all()
        for deal in deals:
            if schedule.slot1 and deal.slot1:
                schedule.slot1 = False
            if schedule.slot2 and deal.slot2:
                schedule.slot2 = False
            if schedule.slot3 and deal.slot3:
                schedule.slot3 = False
            if schedule.slot4 and deal.slot4:
                schedule.slot4 = False


        return render_template("book_worker.html", schedule=schedule)
    @login_required
    def payment(self, id):
        if current_user.user_type != "client":
            return redirect(url_for("user.profile"))
        client_worker_deal = ClientWorkerDeal.query.get(id)
        if client_worker_deal is None:
            # flash("Deal not found", "error")
            return redirect(url_for("client.search_worker"))
        
        worker = Worker.query.get(client_worker_deal.worker_id)

        slot_count = int(client_worker_deal.slot1) + int(client_worker_deal.slot2) + int(client_worker_deal.slot3) + int(client_worker_deal.slot4)

        amount = worker.hourly_rate * slot_count * 4 * 5 * 4 * 100 
        
        # print(amount, worker.hourly_rate, slot_count)
        # slot*4 because per slot 4 hrs. 
        # 4 * 5 because 5 days per week. 4 week per months
        # 100 cause stripe counts in cents.

        if request.method == "POST":
            # CUSTOMER INFO
            customer = stripe.Customer.create(
                email=request.form["stripeEmail"], source=request.form["stripeToken"]
            )

            # PAYMENT INFO
            charge = stripe.Charge.create(
                customer=customer.id, amount=amount, currency="usd", description="Payment"

            )



            # PAYMENT OBJECT
            payment = Payment(
                client_worker_deal_id=client_worker_deal.id,
                amount=amount,
                date=datetime.now(),
            )

            client_worker_deal.active = True

            db.session.add(payment)
            db.session.commit()

            # flash("Payment successful", "success")
            return redirect(url_for("user.profile"))

        return render_template("payment.html", public_key=stripe_keys["public_key"])

    @login_required
    def submit_review(self, id):
        if current_user.user_type != "client":
            return redirect(url_for("user.profile"))
        if request.method == "POST":
            # worker_username = request.form.get("worker_username")
            rating = request.form.get("rating")
            comment = request.form.get("comment")

            worker = Worker.query.get(id)
            if worker is None:
                # flash("Worker not found", "error")
                return redirect(url_for("client.submit_review"))

            review = Review(
                rating=rating,
                comment=comment,
                client_id=current_user.id,
                worker_id=worker.id,
            )

            db.session.add(review)
            db.session.commit()

            return redirect(url_for("user.profile", id=current_user.id))

        return render_template("submit_review.html")
