from flask import Flask, render_template, request, flash
from isolated_f import isolated

app = Flask(__name__)
app.config['SECRET_KEY'] = 'auyst$%gf'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
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
    
    b, d, As, N, s = isolated(dl, ll, col, bc, fck, fyk, bar)

    return render_template('index.html', b=b, d=d, As=As, N=N, s=s, bar=bar)
    

if __name__ == '__main__':
    app.run(debug=True)
