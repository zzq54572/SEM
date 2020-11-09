import os
appdir=os.path.dirname(os.path.abspath(__file__))+'\\..\\..\\'

import sys
sys.path.append(appdir)
from flaskapp import flask_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from script.Log.log import logging,log_stub,add_log_at_begin_and_end

#log=logging

databasedir=os.path.dirname(os.path.abspath(__file__))+'\\..\\..\\datamart\\SQLite\\'
dbfile='''ssoetlmonitor.db'''
#log(os.path.join(basedir, dbfile))


flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(databasedir, dbfile)
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Connects our Flask App to our Database

flask_db = SQLAlchemy(flask_app)
Migrate(flask_app,flask_db)

class Staff(flask_db.Model):
    __tablename__="staff"
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    staff_type=flask_db.Column(flask_db.Text)
    tla=flask_db.Column(flask_db.Text)
    escalation=flask_db.Column(flask_db.Text)
    name=flask_db.Column(flask_db.Text)
    user_id=flask_db.Column(flask_db.Text)
    role=flask_db.Column(flask_db.Text)
    company_division=flask_db.Column(flask_db.Text)
    email=flask_db.Column(flask_db.Text)
    phone=flask_db.Column(flask_db.Text)
    comment=flask_db.Column(flask_db.Text)
    enabled=flask_db.Column(flask_db.Text)
    key_words=flask_db.Column(flask_db.Text)
    def __init__(self,tla="",escalation="",name="",user_id="",role="",company_division="",email="",phone="",comment="",enabled="",key_words=""):
        self.tla=tla
        self.name=name
        self.user_id=user_id
        self.role=role
        self.company_division=company_division
        self.email=email
        self.phone=phone
        self.comment=comment
        self.enabled=enabled
        self.key_words=key_words
    def __repr__(self):
        return "staff["+"(tla:{{.tla}})(name:{{.name}})(role:{{.role}})]"


class Tla(flask_db.Model):
    __tablename__="tla"
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    tla=flask_db.Column(flask_db.Text)
    customer_name=flask_db.Column(flask_db.Text)
    solution=flask_db.Column(flask_db.Text)
    runbook_url=flask_db.Column(flask_db.Text)
    tl=flask_db.Column(flask_db.Text)
    owner=flask_db.Column(flask_db.Text)
    project_code=flask_db.Column(flask_db.Text)
    comment=flask_db.Column(flask_db.Text)
    enabled=flask_db.Column(flask_db.Text)
    key_words=flask_db.Column(flask_db.Text)
    def __init__(self,tla="",customer_name="",solution="",runbook_url="",tl="",owner="",project_code="",comment="",enabled="",key_words=""):
        self.solution=solution
        self.tla=tla
        self.customer_name=customer_name
        self.solution=solution
        self.runbook_url=runbook_url
        self.tl=tl
        self.owner=owner
        self.project_code=project_code
        self.comment=comment
        self.enabled=enabled
        self.key_words=key_words
    def __repr__(self):
        #return "tla["+"(tla:{{.tla}})(customer_name:{{.customer_name}})(solution:{{.solution}})(tl:{{.tl}})(comment:{{.comment}})(enabled:{{.enabled}})(key_words:{{.key_words}})]"
        return f"tla[(tla:{self.tla})(customer_name:{self.customer_name})(solution:{self.solution})(tl:{self.tl})(comment:{self.comment})(enabled:{self.enabled})(key_words:{self.key_words})]"
        
        
class Environment(flask_db.Model):
    __tablename__="environment"
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    tla=flask_db.Column(flask_db.Text)
    deployment_type=flask_db.Column(flask_db.Text)
    server_type=flask_db.Column(flask_db.Text)
    server_machine=flask_db.Column(flask_db.Text)
    terminal_machine=flask_db.Column(flask_db.Text)
    comment=flask_db.Column(flask_db.Text)
    monitored_by=flask_db.Column(flask_db.Text)
    enabled=flask_db.Column(flask_db.Text)
    key_words=flask_db.Column(flask_db.Text)
    is_compliance=flask_db.Column(flask_db.Text)
    def __init__(self,tla="",deployment_type="",server_type="",server_machine="",terminal_machine="",comment="",monitored_by="",enabled="",key_words="",is_compliance=""):
        self.tla=tla
        self.deployment_type=deployment_type
        self.server_type=server_type
        self.server_machine=server_machine
        self.terminal_machine=terminal_machine
        self.comment=comment
        self.monitored_by=monitored_by
        self.enabled=enabled
        self.key_words=key_words
        self.is_compliance=is_compliance
    def __repr__(self):
        return f"tla[(tla:{{self.tla}})(deployment_type:{{self.deployment_type}})(server_type:{{self.server_type}})(machine:{{self.server_machine}})(terminal:{{self.terminal_machine}})(comment:{{self.comment}})(enabled:{{self.enabled}})(key_words:{{self.key_words}})]"

class Crontab(flask_db.Model):
    __tablename__="crontab"
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    tla=flask_db.Column(flask_db.Text)
    deployment_type=flask_db.Column(flask_db.Text)
    machine_name=flask_db.Column(flask_db.Text)
    ip=flask_db.Column(flask_db.Text)    
    crontab_name=flask_db.Column(flask_db.Text)
    minute=flask_db.Column(flask_db.Text)
    hour=flask_db.Column(flask_db.Text)
    day=flask_db.Column(flask_db.Text)
    month=flask_db.Column(flask_db.Text)
    wday=flask_db.Column(flask_db.Text)
    command=flask_db.Column(flask_db.Text)
    enabled=flask_db.Column(flask_db.Text)
    key_words=flask_db.Column(flask_db.Text)
    def __init__(self,tla="",deployment_type="",machine_name="",ip="",crontab_name="",minute="",hour="",day="",month="",wday="",command="",enabled="",key_words=""):
        self.tla=tla
        self.deployment_type=deployment_type
        self.machine_name=machine_name
        self.ip=ip
        self.crontab_name=crontab_name
        self.minute=minute
        self.hour=hour
        self.day=day
        self.month=month
        self.wday=wday
        self.command=command
        self.enabled=enabled
        self.key_words=key_words
    def __repr__(self):
        #return "crontab["+"(tla:{{.tla}})(minute:{{.minute}})(hour:{{.hour}})(day:{{.day}})(month:{{.month}})(wday:{{.wday}})(command:{{.command}})]"
        return f"crontab[(tla:{self.tla})(minute:{self.minute})(hour:{self.hour})(day:{self.day})(month:{self.month})(wday:{self.wday})(command:{self.command})]"

class Schedule(flask_db.Model):
    __tablename__="schedule"
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    tla=flask_db.Column(flask_db.Text)
    datetime=flask_db.Column(flask_db.Text)
    command=flask_db.Column(flask_db.Text)
    crontab=flask_db.Column(flask_db.Text)
    comment=flask_db.Column(flask_db.Text)
    key_words=flask_db.Column(flask_db.Text)
    def __init__(self,tla="",datetime="",command="",crontab="",comment="",key_words=""):
        self.tla=tla
        self.datetime=datetime
        self.command=command
        self.crontab=crontab
        self.enabled=enabled
        self.key_words=key_words
    def __repr__(self):
        return "schedule["+"(tla:{{.tla}})(datetime:{{.datetime}})(command:{{.command}})(crontab:{{.crontab}})(comment:{{.comment}})(key_words:{{.key_words}})]"



class Task(flask_db.Model):
    __tablename__="task"
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    tla=flask_db.Column(flask_db.Text)
    env=flask_db.Column(flask_db.Text)
    assigner=flask_db.Column(flask_db.Text)
    lev=flask_db.Column(flask_db.Text)
    ticket_type=flask_db.Column(flask_db.Text)
    ticket_number=flask_db.Column(flask_db.Text)
    begin_time=flask_db.Column(flask_db.Text)
    end_time=flask_db.Column(flask_db.Text)
    description=flask_db.Column(flask_db.Text)
    enabled=flask_db.Column(flask_db.Text)
    key_words=flask_db.Column(flask_db.Text)


    def __init__(self,tla="",env="",assigner="",lev="",ticket_type="",ticket_number="",begin_time="",end_time="",description="",enabled="",key_words=""):
        self.tla=tla
        self.env=env
        self.assigner=assigner
        self.lev=lev
        self.ticket_type=ticket_type
        self.ticket_number=ticket_number
        self.begin_time=begin_time
        self.end_time=end_time
        self.description=description
        self.enabled=enabled
        self.key_words=key_words

    def __repr__(self):
        return f"task[(tla:{self.tla})(env:{self.env})(assigner:{self.assigner})(lev:{self.lev})(ticket_type:{self.ticket_type})(ticket_number:{self.ticket_number})(begin_time:{self.begin_time})(description:{self.description})(enabled:{self.enabled})(key_words:{self.key_words})]"
    
class Regulation(flask_db.Model):
    __tablename__="regulation"
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    tla=flask_db.Column(flask_db.Text)
    reporter=flask_db.Column(flask_db.Text)
    begin_time=flask_db.Column(flask_db.Text)
    end_time=flask_db.Column(flask_db.Text)
    summary=flask_db.Column(flask_db.Text)
    description=flask_db.Column(flask_db.Text)
    solution=flask_db.Column(flask_db.Text)
    enabled=flask_db.Column(flask_db.Text)
    key_words=flask_db.Column(flask_db.Text)
    def __init__(self,tla="",reporter="",begin_time="",end_time="",summary="",description="",solution="",enabled="",key_words=""):
        self.tla=tla
        self.reporter=reporter
        self.begin_time=begin_time
        self.end_time=end_time
        self.summary=summary
        self.description=description
        self.solution=solution
        self.enabled=enabled 
        self.key_words=key_words
    def __repr__(self):
        return f"regulation[(tla:{self.tla})(reporter:{self.reporter})(summary:{self.summary})(dscription:{self.description})(solutino:{self.solution})(key_words:{self.key_words})]"

class RutineOpt(flask_db.Model):
    __tablename__="rutineopt"
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    tla=flask_db.Column(flask_db.Text)
    reporter=flask_db.Column(flask_db.Text)
    begin_time=flask_db.Column(flask_db.Text)
    description=flask_db.Column(flask_db.Text)
    enabled=flask_db.Column(flask_db.Text)
    key_words=flask_db.Column(flask_db.Text)
    def __init__(self,tla="",reporter="",begin_time="",description="",enabled="",key_words=""):
        self.tla=tla
        self.reporter=reporter
        self.begin_time=begin_time
        self.description=description
        self.enabled=enabled 
        self.key_words=key_words
    def __repr__(self):
        return "rutineopt["+"(tla:{{.tla}})(reporter:{{.reporter}})(begin_time:{{.begin_time}})(description:{{.description}})(enabled:{{.enabled}})(key_words:{{.key_words}})]"    


class Issue(flask_db.Model):
    __tablename__="issue"
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    tla=flask_db.Column(flask_db.Text)
    ticket_type=flask_db.Column(flask_db.Text)
    ticket_number=flask_db.Column(flask_db.Text)
    begin_time=flask_db.Column(flask_db.Text)
    description=flask_db.Column(flask_db.Text)
    enabled=flask_db.Column(flask_db.Text)
    key_words=flask_db.Column(flask_db.Text)
    def __init__(self,tla="",ticket_type="",ticket_number="",begin_time="",description="",enabled="",key_words=""):
        self.tla=tla
        self.ticket_type=ticket_type
        self.ticket_number=ticket_number
        self.begin_time=begin_time
        self.description=description
        self.enabled=enabled
        self.key_words=key_words
    def __repr__(self):
        return "issue["+"(tla:{{.tla}})(ticket_type:{{.ticket_type}})(ticket_number:{{.ticket_number}})(begin_time:{{.begin_time}})(description:{{.description}})(enabled:{{.enabled}})(key_words:{{.key_words}})]"
class ComplianceReport(flask_db.Model):
    __tablename__="compliance_report" 
    id=flask_db.Column(flask_db.Integer,primary_key=True)
    tla=flask_db.Column(flask_db.Text)
    deployment_type=flask_db.Column(flask_db.Text)
    status=flask_db.Column(flask_db.Text)
    is_respond=flask_db.Column(flask_db.Text)
    ticket=flask_db.Column(flask_db.Text)
    small_file=flask_db.Column(flask_db.Text)
    task=flask_db.Column(flask_db.Text)
    comment=flask_db.Column(flask_db.Text)
    def __init__(self,tla="",deployment_type="",status="",is_respond="",ticket="",small_file="",task="",comment=""):
        self.tla=tla
        self.deployment_type=deployment_type
        self.status=status
        self.is_respond=is_respond
        self.ticket=ticket
        self.small_file=small_file
        self.task=task
        self.comment=comment
    def __repr__(self):
        return f'{{self.tla}}:{{self.status}}'
    
    
    
    
def add_row(record):
    db.session.add(record)
    db.session.commit()       
       
def add_rows(records):
    db.session.add_all(records)
    db.session.commit()

def query_row(model,tla):
    if tla=="":
        return model.query.get(1)
    else:
        return model.query.filter_by(tla=tla).first()


def query_rows(model,tla):
    #return model.query.all()
    return model.query.filter_by(tla=tla).all()
  

def query_rows_all(model):
    return model.query.all()  

