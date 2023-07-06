from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['Get', 'POST'])
def result():
    number = request.form['number']
    string = request.form['string']
    result = int(number) * 2
    capitalized_string = string.upper()
    return redirect('/display_result/' + str(result) + '/' + capitalized_string)

@app.route('/display_result/<result>/<capitalized_string>')
def display_result(result, capitalized_string):
    return render_template('result.html', result=result, capitalized_string=capitalized_string)

if __name__ == '__main__':
    app.run(debug=True)

