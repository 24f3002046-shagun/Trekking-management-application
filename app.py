from flask import Flask
from backend.models import *
from flask_login import LoginManager

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///tma.sqlite3"
    app.config["SECRET_KEY"] = "trek-secret-key"
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    db.init_app(app)
    @login_manager.user_loader
    def load_user(email):
        return User.query.filter_by(email=email).first()
    app.app_context().push()
    return app

app=create_app()
from backend.routes import *
from backend.create_initial_data import *

if __name__=="__main__":
    app.run(debug=True)