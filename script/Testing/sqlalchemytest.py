import sys
sys.path.append("..\\")
sys.path.append("..\\..\\")
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskapp import flask_app

basedir=os.path.dirname(os.path.abspath(__file__))+'\\..\\..\\datamart\\SQLite\\'
dbfile='''ssoetlmonitor.db'''


flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, dbfile)
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Connects our Flask App to our Database

flask_db = SQLAlchemy(flask_app)


class Task(flask_db.Model):
    __tablename__ = "task"
    id = flask_db.Column(flask_db.Integer, primary_key=True)
    tla = flask_db.Column(flask_db.Text)
    env = flask_db.Column(flask_db.Text)
    assigner = flask_db.Column(flask_db.Text)
    lev = flask_db.Column(flask_db.Text)
    ticket_type = flask_db.Column(flask_db.Text)
    ticket_number = flask_db.Column(flask_db.Text)
    begin_time = flask_db.Column(flask_db.Text)
    end_time = flask_db.Column(flask_db.Text)
    description = flask_db.Column(flask_db.Text)
    enabled = flask_db.Column(flask_db.Text)
    key_words = flask_db.Column(flask_db.Text)

    def __init__(self, tla="", env="", assigner="", lev="", ticket_type="", ticket_number="", begin_time="",
                 end_time="", description="", enabled="", key_words=""):
        self.tla = tla
        self.env = env
        self.assigner = assigner
        self.lev = lev
        self.ticket_type = ticket_type
        self.ticket_number = ticket_number
        self.begin_time = begin_time
        self.end_time = end_time
        self.description = description
        self.enabled = enabled
        self.key_words = key_words

    def __repr__(self):
        return f"task[(tla:{self.tla})(env:{self.env})(assigner:{self.assigner})(lev:{self.lev})(ticket_type:{self.ticket_type})(ticket_number:{self.ticket_number})(begin_time:{self.begin_time})(description:{self.description})(enabled:{self.enabled})(key_words:{self.key_words})]"


rows=Task.query.all()
for row in rows:
    print(row)