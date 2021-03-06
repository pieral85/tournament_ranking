from flask import Flask
# from ..tools import points_matrix

# app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config') # Now we can access the configuration variables via app.config["VAR_NAME"].
# Load the configuration from the `instance` folder
app.config.from_pyfile('config.py')


from flask_debugtoolbar import DebugToolbarExtension

toolbar = DebugToolbarExtension(app)  # TODO Does not seem to be working...delete me in this case






# =========== db ===========
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print(app.config['SQLALCHEMY_DATABASE_URI'])
# import ipdb; ipdb.set_trace()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)#, convert_unicode=True)  # , echo=False)
 
# create a Declarative base class which stores the classes representing tables
Base = declarative_base()
# Base.metadata.reflect(bind=engine)#TODO Not working: check if it is useful
# Base.query = db_session.query_property()#TODO useful???

# -----------------------
# from sqlalchemy.orm import scoped_session
# import ipdb; ipdb.set_trace()
# Session = scoped_session(sessionmaker())
# Session.configure(bind=engine)
# Base.metadata.bind = engine
# -----------------------

 
# create a configured "Session" class
Session = sessionmaker(bind=engine)
 
# create a Session
session = Session()
 
# create all tables that don't yet exist
# Base.metadata.create_all(engine)
# ==========================



# This import must be done after creation of `Base`,
# as all models files import `Base` variable
from .main.controllers import main


app.register_blueprint(main, url_prefix='/')


# def create_app(config_filename):
#     app = Flask(__name__)
#     app.config.from_pyfile(config_filename)

#     # from yourapplication.model import db
#     # from .db import init_db
#     import db
#     db.init_app(app)???

#     # from yourapplication.views.admin import admin
#     # from yourapplication.views.frontend import frontend
#     # app.register_blueprint(admin)
#     # app.register_blueprint(frontend)

#     return app


# Following code structuration has been found here:
# https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

# Import flask and template operators
# from flask import Flask, render_template

# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
# app = Flask(__name__)

# Configurations
# app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
# db = SQLAlchemy(app)

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
# from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
# app.register_blueprint(auth_module)
# # app.register_blueprint(xyz_module)
# # ..

# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()
