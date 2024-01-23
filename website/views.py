""" main views module """


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
def home():
    """ for home page """
    return render_template('home.html', user=current_user)


@views.route('/about')
def about():
    """ for abouts page """
    return render_template('about.html', user=current_user)


@views.route('/faq')
def faq():
    """ for FAQ page """
    return render_template('faq.html', user=current_user)


@views.route('/found_type', methods=['GET', 'POST'])
def found_type():
    """ allows selection of foundation type """
    if request.method == 'POST': 
        option = request.form['option']
        if option == 'iso_square':
            return redirect(url_for('views.soil_type'))
    return render_template('found_type.html', user=current_user)


@views.route('/soil_type', methods=['GET', 'POST'])
def soil_type():
    """ allows selection of soil type """
    if request.method == 'POST': 
        option = request.form['option']
        if option == 'clay':
            return render_template('clay.html', user=current_user)
        elif option == 'sand':
            return render_template('sand.html', user=current_user)
        elif option == 'bearing_c':
            return render_template('bearing_c.html', user=current_user)
    return render_template('soil_type.html', user=current_user)


@views.route('/clay_soil_results', methods=['POST'])
def clay_soil_results():
    """ takes inputs and displays results for clay soil """
    dl = request.form['DL']
    ll = request.form['LL']
    col = request.form['COL']
    cu = request.form['CU']
    df = request.form['DF']
    gam = request.form['GAM']
    fck = request.form['FCK']
    fyk = request.form['FYK']
    bar = request.form['BAR']
    cov = request.form['COV']
    var_list = [dl, ll, col, cu, df, gam, fck, fyk, bar, cov]
	
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
	
    if any(not var for var in var_list):
        flash('An input field is blank.', category='error')
    elif any(not is_float(var) for var in var_list):    
        flash('An input field is not a number.', category='error')
    else:
        dl = float(request.form['DL'])
        ll = float(request.form['LL'])
        col = float(request.form['COL'])
        cu = float(request.form['CU'])
        df = float(request.form['DF'])
        gam = float(request.form['GAM'])
        fck = float(request.form['FCK'])
        fyk = float(request.form['FYK'])
        bar = float(request.form['BAR'])
        cov = float(request.form['COV'])
        submit_type = request.form['submit_type']
        user = current_user
        b, d, As, N, s, qa, fs, qu = clay_iso(dl, ll, col, cu, df, gam, fck, fyk, bar, cov)
        if submit_type == 'regular':
            if b == 0:
                return render_template('result.html', text="You", user=current_user)
            else:
                return render_template('result.html', b=b, d=d, N=N, s=s, bar=bar,\
                        user=current_user)
        elif submit_type == 'advanced':
            if user.is_authenticated:
                if b == 0:
                    return render_template('result.html', text="You", user=current_user)
                else:
                    return render_template('result_adv.html', b=b, d=d, As=As, N=N, s=s,\
                            qa=qa, fs=fs, qu=qu, dl=dl, ll=ll, col=col, cu=cu, df=df, gam=gam, fck=fck,\
                            fyk=fyk, bar=bar, cov=cov, user=current_user)
            else:
                return redirect(url_for('auth.login'))
    return render_template('clay.html', user=current_user)


@views.route('/sand_soil_results', methods=['POST'])
def sand_soil_results():
    """ takes inputs and displays results for sand soil """
    dl = request.form['DL']
    ll = request.form['LL']
    col = request.form['COL']
    phi = request.form['PHI']
    df = request.form['DF']
    gam = request.form['GAM']
    fck = request.form['FCK']
    fyk = request.form['FYK']
    bar = request.form['BAR']
    cov = request.form['COV']
    var_list = [dl, ll, col, phi, df, gam, fck, fyk, bar, cov]
	
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
	
    if any(not var for var in var_list):
        flash('An input field is blank.', category='error')
    elif any(not is_float(var) for var in var_list):    
        flash('An input field is not a number.', category='error')
    else:
        dl = float(request.form['DL'])
        ll = float(request.form['LL'])
        col = float(request.form['COL'])
        phi = float(request.form['PHI'])
        df = float(request.form['DF'])
        gam = float(request.form['GAM'])
        fck = float(request.form['FCK'])
        fyk = float(request.form['FYK'])
        bar = float(request.form['BAR'])
        cov = float(request.form['COV'])
        submit_type = request.form['submit_type']
        user = current_user
        b, d, As, N, s, qa, fs, qu = sand_iso(dl, ll, col, phi, df, gam, fck, fyk, bar, cov)
        if submit_type == 'regular':
            if b == 0:
                return render_template('result.html', text="You", user=current_user)
            else:
                return render_template('result.html', b=b, d=d, N=N, s=s, bar=bar,\
                        user=current_user)
        elif submit_type == 'advanced':
            if user.is_authenticated:
                if b == 0:
                    return render_template('result.html', text="You", user=current_user)
                else:
                    return render_template('result_adv.html', b=b, d=d, As=As, N=N, s=s,\
                            qa=qa, fs=fs, qu=qu, dl=dl, ll=ll, col=col, phi=phi, df=df, gam=gam, fck=fck,\
                            fyk=fyk, bar=bar, cov=cov, user=current_user)
            else:
                return redirect(url_for('auth.login'))
    return render_template('sand.html', user=current_user)


@views.route('/bearing_cap_results', methods=['POST'])
def bearing_cap_results():
    """ takes inputs and displays results when bearing capacity is provided """
    dl = request.form['DL']
    ll = request.form['LL']
    col = request.form['COL']
    bc = request.form['BC']
    fck = request.form['FCK']
    fyk = request.form['FYK']
    bar = request.form['BAR']
    cov = request.form['COV']
    var_list = [dl, ll, col, bc, fck, fyk, bar, cov]
	
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
	
    if any(not var for var in var_list):
        flash('An input field is blank.', category='error')
    elif any(not is_float(var) for var in var_list):    
        flash('An input field is not a number.', category='error')
    else:
        dl = float(request.form['DL'])
        ll = float(request.form['LL'])
        col = float(request.form['COL'])
        bc = float(request.form['BC'])
        fck = float(request.form['FCK'])
        fyk = float(request.form['FYK'])
        bar = float(request.form['BAR'])
        cov = float(request.form['COV'])
        submit_type = request.form['submit_type']
        user = current_user
        b, d, As, N, s = bearing_c_iso(dl, ll, col, bc, fck, fyk, bar, cov)
        if submit_type == 'regular':
            if b == 0:
                return render_template('result.html', text="You", user=current_user)
            else:
                return render_template('result.html', b=b, d=d, N=N, s=s, bar=bar,\
                        user=current_user)
        elif submit_type == 'advanced':
            if user.is_authenticated:
                if b == 0:
                    return render_template('result.html', text="You", user=current_user)
                else:
                    return render_template('result_adv.html', b=b, d=d, As=As, N=N, s=s,\
                            dl=dl, ll=ll, col=col, bc=bc, fck=fck,\
                            fyk=fyk, bar=bar, cov=cov, user=current_user)
            else:
                return redirect(url_for('auth.login'))
    return render_template('bearing_c.html', user=current_user)
    

@views.route('/save', methods=['GET', 'POST'])
@login_required
def save():
    """ saves users advanced results """
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("saved.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    """ deletes the saved advanced results """
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
