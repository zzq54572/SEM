import sys
sys.path.append("..")
sys.path.append("..\\..")
from Database.database import *
from time import time,localtime
#from Log.log import logging,log_stub,add_log_at_begin_and_end

#import os
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
#from flaskapp import flask_app
#from script.Log.log import logging,log_stub,add_log_at_begin_and_end
#log=logging


#basedir='''C:\WorkSpace\PythonProgram\SSOETLMonitor'''
#basedir=os.path.dirname(os.path.abspath(__file__))+'\\..\\..\\datamart\\SQLite\\'
#dbfile='''ssoetlmonitor.db'''
#log(os.path.join(basedir, dbfile))


#flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, dbfile)
#flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Connects our Flask App to our Database

#flask_db = SQLAlchemy(flask_app)



#class Tla1(flask_db.Model):
#    __tablename__="tla"
#    id=flask_db.Column(flask_db.Integer,primary_key=True)
#    tla=flask_db.Column(flask_db.Text)
#    customer_name=flask_db.Column(flask_db.Text)
#    solution=flask_db.Column(flask_db.Text)
#    runbook_url=flask_db.Column(flask_db.Text)
#    tl=flask_db.Column(flask_db.Text)
#    project_code=flask_db.Column(flask_db.Text)
#    comment=flask_db.Column(flask_db.Text)
#    enabled=flask_db.Column(flask_db.Text)
#    key_words=flask_db.Column(flask_db.Text)
#    def __init__(self,tla="",customer_name="",solution="",runbook="",tl="",project_code="",comment="",enabled="",key_words=""):
#        self.solution=solution
#        self.tla=tla
#        self.customer_name=customer_name
#        self.solution=solution
#        self.runbook_url=runbook_url
#        self.tl=tl
#        self.project_code=project_code
#        self.comment=comment
#        self.enabled=enabled
#        self.key_words=key_words
#    def __repr__(self):
#        return "tla["+"(tla:{self.tla})(customer_name:{self.customer_name})(solution:{self.solution})(tl:{self.tl})(comment:{self.comment})(enabled:{self.enabled})(key_words:{self.key_words})]"
#        return f"tla[(tla:{self.tla})(customer_name:{self.customer_name})(solution:{self.solution})(tl:{self.tl})(comment:{self.comment})(enabled:{self.enabled})(key_words:{self.key_words})]"


#rows=ComplianceReport.query.filter_by(tla="BLS")
def query_environments():
    report=Environment.query.all()
    return report
rows = query_environments()
for a in rows:
    print([a.tla,a.deployment_type])