from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from .models import ProfileData
from .models import FuelOrderFormData
from . import db
import json
import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    if current_user.is_authenticated:
        profile = ProfileData.query.filter_by(id=current_user.id).first()
    else:
        profile = None

    return render_template("home.html", user=current_user, profile=profile)


@views.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    profile = ProfileData.query.filter_by(id=current_user.id).first()

    if request.method == 'POST':
        full_name = request.form['full_name']
        address_1 = request.form['address_1']
        address_2 = request.form['address_2']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']

        # TODO: Add server-side validation for the form fields

        in_state_status = (state == "TX")

        if profile is None:
            profile = ProfileData(id=current_user.id)
            db.session.add(profile)

        profile.full_name = full_name
        profile.address_1 = address_1
        profile.address_2 = address_2
        profile.city = city
        profile.state = state
        profile.in_state_status = in_state_status
        profile.zip_code = zip_code
        profile.profile_completed = True  # Set profile_completed to True

        db.session.commit()
        flash("Profile completed successfully!")

        return redirect(url_for('views.complete_profile'))

    return render_template("complete_profile.html", user=current_user, profile=profile)

@views.route('/view_history', methods=['GET'])
@login_required
def view_history():
    profile = ProfileData.query.filter_by(id=current_user.id).first()
    orders = FuelOrderFormData.query.filter_by(user_id=current_user.id).all()
    return render_template("view_history.html", user=current_user, profile=profile, orders=orders)


@views.route('/fuel_price_form', methods=['GET', 'POST'])
@login_required
def fuel_price_form():
    profile = ProfileData.query.filter_by(id=current_user.id).first()
    price = None  # Initialize the price variable

    if request.method == 'POST':
        gallons = float(request.form['gallons_requested'])  # Convert to float
        delivery_date = request.form['delivery_date']

        delivery_date = datetime.datetime.strptime(delivery_date, '%Y-%m-%d').date()
        
        is_new_customer = FuelOrderFormData.query.filter_by(user_id=current_user.id).first() is None

        if profile.in_state_status:
            location_fee = 5
        else:
            location_fee = 15

        if is_new_customer:
            discount_rate = 0
        else:
            discount_rate = -0.20

        company_profit_margin = ((-1.50 * gallons) + (3.36 * gallons)) / abs(((-1.50 * gallons) + (3.36 * gallons)))

        if company_profit_margin == 0:
            profit_fee = 1.00
        elif company_profit_margin >= 1:
            profit_fee = 0.50
        else:
            profit_fee = 2.00

        price = (3.36 * gallons) + (gallons * location_fee) + (gallons * discount_rate) + (gallons * profit_fee)
        price_per_gallon = 3.36 + location_fee + discount_rate + profit_fee

        fuel_order_form_data = FuelOrderFormData(
            gallons=gallons,
            delivery_date=delivery_date,
            address_1=profile.address_1,
            address_2=profile.address_2,
            city=profile.city,
            state=profile.state,
            zip_code=profile.zip_code,
            price=price,
            user=current_user
        )

        db.session.add(fuel_order_form_data)
        db.session.commit()

        flash("Fuel ordered successfully!")

        return render_template(
            "fuel_price_form.html",
            user=current_user,
            profile=profile,
            price=price,
            address_1=profile.address_1,
            price_per_gallon=price_per_gallon
        )

    return render_template("fuel_price_form.html", user=current_user, profile=profile, price=price)

