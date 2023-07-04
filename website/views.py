from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from .bearing_c import bearing_c_iso
from .clay import clay_iso
from .sand import sand_iso

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html', user=current_user)

@views.route('/inputs', methods=['POST'])
def inputs():
    option = request.form['option']
    if option == 'clay':
        return render_template('clay.html', user=current_user)
    elif option == 'sand':
        return render_template('sand.html', user=current_user)
    elif option == 'bearing_c':
        return render_template('bearing_c.html', user=current_user)

@views.route('/clay_soil_results', methods=['POST'])
def clay_soil_results():
    dl = request.form['DL']
    ll = request.form['LL']
    col = request.form['COL']
    cu = request.form['CU']
    df = request.form['DF']
    gam = request.form['GAM']
    fck = request.form['FCK']
    fyk = request.form['FYK']
    bar = request.form['BAR']
    if not dl or not ll or not col or not bc or not fck or not fyk:
        flash('An input field can not be blank.', category='error')
    elif any(not isinstance(x, (int, float)) for x in (dl, ll, col, bc, fck, fyk)):
        flash('An input field has to be a number.', category='error')
    else:
        flash('Calculation successful!', category='success')
    
    dl = float(request.form['DL'])
    ll = float(request.form['LL'])
    col = float(request.form['COL'])
    cu = float(request.form['CU'])
    df = float(request.form['DF'])
    gam = float(request.form['GAM'])
    fck = float(request.form['FCK'])
    fyk = float(request.form['FYK'])
    bar = float(request.form['BAR'])
    submit_type = request.form['submit_type']
    user = current_user
    b, d, As, N, s = clay_iso(dl, ll, col, cu, df, gam, fck, fyk, bar)
    if submit_type == 'regular':
        return render_template('result.html', b=b, d=d, As=As, N=N, s=s,\
                user=current_user)
    elif submit_type == 'advanced':
        if user.is_authenticated:
            return render_template('result_adv.html', b=b, d=d, As=As, N=N, s=s,\
                    dl=dl, ll=ll, col=col, cu=cu, df=df, gam=gam, fck=fck,\
                    fyk=fyk, bar=bar, user=current_user)
        else:
            return redirect(url_for('auth.login'))

@views.route('/sand_soil_results', methods=['POST'])
def sand_soil_results():
    dl = float(request.form['DL'])
    ll = float(request.form['LL'])
    col = float(request.form['COL'])
    phi = float(request.form['PHI'])
    df = float(request.form['DF'])
    gam = float(request.form['GAM'])
    fck = float(request.form['FCK'])
    fyk = float(request.form['FYK'])
    bar = float(request.form['BAR'])
    b, d, As, N, s = sand_iso(dl, ll, col, phi, df, gam, fck, fyk, bar)
    return render_template('result.html', b=b, d=d, As=As, N=N, s=s,\
            dl=dl, ll=ll, col=col, phi=phi, df=df, gam=gam, fck=fck,\
            fyk=fyk, bar=bar, user=current_user)

@views.route('/bearing_cap_results', methods=['POST'])
def bearing_cap_results():
    dl = float(request.form['DL'])
    ll = float(request.form['LL'])
    col = float(request.form['COL'])
    bc = float(request.form['BC'])
    fck = float(request.form['FCK'])
    fyk = float(request.form['FYK'])
    bar = float(request.form['BAR'])

    b, d, As, N, s = bearing_c_iso(dl, ll, col, bc, fck, fyk, bar)
    return render_template('result.html', b=b, d=d, As=As, N=N, s=s,\
            dl=dl, ll=ll, col=col, bc=bc, fck=fck, fyk=fyk, bar=bar, user=current_user)
    

@views.route('/home', methods=['GET', 'POST'])
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