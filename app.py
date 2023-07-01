from flask import Flask, render_template, request, flash
from bearing_c import bearing_c_iso
from clay import clay_iso
from sand import sand_iso

app = Flask(__name__)
app.config['SECRET_KEY'] = 'acyst$%gf'

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
