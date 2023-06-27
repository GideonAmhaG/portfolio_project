from flask import Flask, render_template, request
from isolated_f import isolated

app = Flask(__name__)

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

    b, d, As, N, s = isolated(dl, ll, col, bc, fck, fyk)

    return render_template('index.html', b=b, d=d, As=As, N=N, s=s)

if __name__ == '__main__':
    app.run(debug=True)
