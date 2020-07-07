from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView
#from app.models import User, Post
from flaskext.markdown import Markdown
from flask_login import LoginManager


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager()

login.login_view = 'login'

login.login_message_category = 'info'

login.login_message = 'Access denied.'

login.init_app(app)

Markdown(app)
migrate = Migrate(app,db)

#admin = Admin(app)
#admin.add_View(ModelView(User, db.session))
#admin.add_View(ModelView(Post, db.session))

from app import routes, models
from app.models import User_, query_user

@login.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User_()
        curr_user.id = user_id

        return curr_user