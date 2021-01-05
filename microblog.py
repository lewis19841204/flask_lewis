from app import app
from datetime import datetime
from app.models import User,Post


@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Post':Post}

if __name__== '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
