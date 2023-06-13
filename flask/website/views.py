from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from .models import ProfileData
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
        
        profile_data = ProfileData(full_name=full_name, address_1=address_1,
                                  address_2=address_2, 
                                  city=city,
                                  state=state,
                                  zip_code=zip_code)
        db.session.add(profile_data)
        db.session.commit()
        flash("Profile completed successfully!")
        
        return redirect(url_for('views.complete_profile', user=current_user))
    
    return render_template("complete_profile.html", user=current_user)
