from flask import Flask, render_template, request
import calculate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    num1 = int(request.form['number1'])
    num2 = int(request.form['number2'])
    num3 = int(request.form['number3'])
    num4 = int(request.form['number4'])

    results = calculate.calculate_all(num1, num2, num3, num4)

    result1 = results[0]
    result2 = results[1]
    result3 = results[2]
    result4 = results[3]

    return render_template('index.html', result1=result1, result2=result2, result3=result3, result4=result4)

if __name__ == '__main__':
    app.run(debug=True)

