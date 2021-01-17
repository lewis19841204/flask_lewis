from flask import Flask,render_template,request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random')
def genbum():
    maxnum = request.args.get('max')
    value = random.randint(0, int(maxnum))
    return str(value)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5555)
