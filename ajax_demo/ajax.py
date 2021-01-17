from flask import Flask,render_template,request,jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/random')
def genbum():
    maxnum = request.args.get('max')
    value = random.randint(0, int(maxnum))
    return str(value)

@app.route('/checkUser',methods=['get','post'])
def checkUser():
    usernames = ['lewis','lucy']
    username =request.form.get('username')
    res = {'flag':0} #用户不存在可以注册
    if username in usernames:
        res['flag'] = 1

    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5555)
