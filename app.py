from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from bearing_c import bearing_c_iso
from clay import clay_iso
from sand import sand_iso

app = Flask(__name__)
app.config['SECRET_KEY'] = 'acyst$%gf'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('adv_results'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('adv_results'))
    return render_template("sign_up.html", user=current_user)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inputs', methods=['POST'])
def inputs():
    option = request.form['option']
    if option == 'clay':
        return render_template('clay.html')
    elif option == 'sand':
        return render_template('sand.html')
    elif option == 'bearing_c':
        return render_template('bearing_c.html')

@app.route('/clay_soil_results', methods=['POST'])
def clay_soil_results():
    dl = float(request.form['DL'])
    ll = float(request.form['LL'])
    col = float(request.form['COL'])
    cu = float(request.form['CU'])
    df = float(request.form['DF'])
    gam = float(request.form['GAM'])
    fck = float(request.form['FCK'])
    fyk = float(request.form['FYK'])
    bar = float(request.form['BAR'])
    b, d, As, N, s = clay_iso(dl, ll, col, cu, df, gam, fck, fyk, bar)
    return render_template('result.html', b=b, d=d, As=As, N=N, s=s,\
            dl=dl, ll=ll, col=col, cu=cu, df=df, gam=gam, fck=fck,\
            fyk=fyk, bar=bar)

@app.route('/sand_soil_results', methods=['POST'])
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
            fyk=fyk, bar=bar)

@app.route('/bearing_cap_results', methods=['POST'])
def bearing_cap_results():
    dl = float(request.form['DL'])
    ll = float(request.form['LL'])
    col = float(request.form['COL'])
    bc = float(request.form['BC'])
    fck = float(request.form['FCK'])
    fyk = float(request.form['FYK'])
    bar = float(request.form['BAR'])

    """if not dl or not ll or not col or not bc or not fck or not fyk:
        flash('An input field can not be blank.', category='error')
    elif any(not isinstance(x, (int, float)) for x in (dl, ll, col, bc, fck, fyk)):
        flash('An input field has to be a number.', category='error')
    else:
        flash('Calculation successful!', category='success')"""
    
    b, d, As, N, s = bearing_c_iso(dl, ll, col, bc, fck, fyk, bar)
    return render_template('result.html', b=b, d=d, As=As, N=N, s=s,\
            dl=dl, ll=ll, col=col, bc=bc, fck=fck, fyk=fyk, bar=bar)
    

if __name__ == '__main__':
    app.run(debug=True)
