from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import ProfileData
from .models import FuelOrderFormData
from . import db
import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    profile = ProfileData.query.filter_by(id=current_user.id).first()

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

        # Server-side input validation
        errors = []

        if not full_name:
            errors.append("Full name is required.")

        if not address_1:
            errors.append("Address line 1 is required.")

        if not city:
            errors.append("City is required.")

        if not state:
            errors.append("State is required.")

        if not zip_code:
            errors.append("ZIP code is required.")

        if errors:
            # If there are validation errors, render the template again with the errors.
            return render_template("complete_profile.html", user=current_user, profile=profile, errors=errors)

        # If there are no validation errors, update the profile and commit the changes.
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

        return redirect(url_for('views.home'))

    return render_template("complete_profile.html", user=current_user, profile=profile)

@views.route('/view_history', methods=['GET'])
@login_required
def view_history():
    profile = ProfileData.query.filter_by(id=current_user.id).first()
    orders = FuelOrderFormData.query.filter_by(user_id=current_user.id).all()
    return render_template("view_history.html", user=current_user, profile=profile, orders=orders)


def validate_delivery_date(delivery_date):
    delivery_date = datetime.datetime.strptime(delivery_date, '%Y-%m-%d').date()
    current_date = datetime.date.today()

    if delivery_date < current_date:
        print("Delivery date cannot be in the past.")

@views.route('/fuel_price_form', methods=['GET', 'POST'])
@login_required
def fuel_price_form():
    profile = ProfileData.query.filter_by(id=current_user.id).first()

    if request.method == 'POST':
        price = None  # Initialize the price variable
        gallons = float(request.form['gallons_requested'])  # Convert to float
        if gallons < 1:
            flash("Gallons requested must be greater than or equal to 1!", category="error")
            return render_template("fuel_price_form.html", user=current_user, profile=profile, price=price, price_per_gallon=None)
        delivery_date = request.form['delivery_date']

        validate_delivery_date(delivery_date)

        delivery_date = datetime.datetime.strptime(delivery_date, '%Y-%m-%d').date()
        
        is_new_customer = FuelOrderFormData.query.filter_by(user_id=current_user.id).first() is None

        current_price = 1.50
        profit_factor = 0.10
           
        if profile.in_state_status:
            location_factor = 0.02
        else:
            location_factor = 0.04

        if is_new_customer:
            history_factor = 0
        else:
            history_factor = 0.01

        if gallons > 1000:
            requested_factor = 0.02
        else:
            requested_factor = 0.03

        company_profit_margin = current_price * (location_factor - history_factor + requested_factor + profit_factor)


        price_per_gallon = current_price + company_profit_margin
        price = gallons * price_per_gallon

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

        return render_template(
            "fuel_price_form.html",
            user=current_user,
            profile=profile,
            price=price,
            address_1=profile.address_1,
            price_per_gallon=price_per_gallon
        )

    return render_template("fuel_price_form.html", user=current_user, profile=profile, price=None, price_per_gallon=None)

