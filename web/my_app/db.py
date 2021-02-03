# #TODO Delete this file if not used (db setup is done in /web/my/app/__init__.py)

# # Some help can be found here:
# #https://zaxrosenberg.com/flask-set-up-sqlalchemy-orm-vs-flask_sqlalchemy-orm/

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# # engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
# engine = create_engine("access+pyodbc://Admin:.......@acces_test_tp", convert_unicode=True)  # , echo=False)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()

# # create database  # TODO delete if not needed
# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     import ipdb; ipdb.set_trace()
#     from models import club, draw, entry, event, link, match, player
#     import yourapplication.models
#     Base.metadata.create_all(bind=engine)


