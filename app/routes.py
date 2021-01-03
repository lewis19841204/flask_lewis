from app import app   #从app包中导入Flask程序对象的实例app

#two routes,无论输入以下哪个URL路由，都会进入def index()函数中

@app.route('/')
@app.route('/index')

#one view_function
def index():
    return 'Hello,world!'
