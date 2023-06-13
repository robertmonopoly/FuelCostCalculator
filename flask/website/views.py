from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from .models import ProfileData
from .models import FuelOrderFormData
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/complete_profile', methods=['GET', 'POST'])
def complete_profile():
    if request.method == 'POST':
        full_name = request.form['full_name']
        address_1 = request.form['address_1']
        address_2 = request.form['address_2']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']

        in_state_status = True
        if state != "TX":
            in_state_status = False

        new_customer_status = True    
        
        profile_data = ProfileData(full_name=full_name, address_1=address_1,
                                  address_2=address_2, 
                                  city=city,
                                  state=state,
                                  in_state_status=in_state_status,
                                  zip_code=zip_code,
                                  new_customer_status=new_customer_status)
        db.session.add(profile_data)
        db.session.commit()
        flash("Profile completed successfully!")
        
        return redirect(url_for('views.complete_profile', user=current_user))
    
    return render_template("complete_profile.html", user=current_user)

@views.route('/fuel_price_form', methods=['GET', 'POST'])
def fuel_price_form():
    if request.method == 'POST':
        gallons = request.form['gallons_requested']
        delivery_date = request.form['delivery_date']
        
        if in_state_status == True:
            location_fee = 5
        else:
            location_fee = 15
        
        if new_customer_status == True:
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

        total_cost = (3.36 * gallons) + (gallons * location_fee) + (gallons * discount_rate) + (gallons * profit_fee)

        
        fuel_order_form_data = FuelOrderFormData(
                                gallons=gallons,
                                delivery_date=delivery_date,
                                full_name=full_name, 
                                address_1=address_1,
                                address_2=address_2, 
                                city=city,
                                state=state,
                                in_state_status=in_state_status,
                                zip_code=zip_code,
                                price=total_cost)
        db.session.add(fuel_order_form_data)
        db.session.commit()
        flash("Fuel ordered successfully!")
        
        return redirect(url_for('views.fuel_price_form', user=current_user))
    
    return render_template("fuel_price_form.html", user=current_user)
