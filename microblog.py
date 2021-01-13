from app import app,db
from datetime import datetime
from app.models import User,Post
from app.forms import LoginForm,RegistrationForm,ResetPasswordRequestForm,EditProfileForm,ResetPasswordForm 

@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Post':Post}

if __name__== '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
