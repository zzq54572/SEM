import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from CommonHandler import *

from database import *



from time import time, localtime
#from script.Log.log import *
from sqlalchemy import func




def query_regulation_all():
    all_regulation = query_rows_all(Regulation)
    return all_regulation


def query_regulation_by_tla(tla):
    # 使用ilike而不是like查询时 username 字段就不会区分大小写了
    all_regulation = Regulation.query.filter(Regulation.tla.ilike(f'%{tla}%')).all()
    return all_regulation


def query_regulation_by_tla_unique(tla):
    all_regulation = Regulation.query.filter(func.lower(Regulation.tla) == func.lower(tla)).all()
    return all_regulation


def query_regulation_by_id(id):
    regulation = Regulation.query.filter_by(id=id).first()
    return regulation

def update_regulation(new_regulation):
    regulation = Regulation.query.filter_by(id=new_regulation.id).first()
    #print("update tla:", type(tla), tla)
    regulation.id = new_regulation.id
    regulation.tla = new_regulation.tla
    regulation.reporter = new_regulation.reporter
    regulation.begin_time = new_regulation.begin_time
    regulation.end_time = new_regulation.end_time
    regulation.summary = new_regulation.summary
    regulation.description = new_regulation.description
    regulation.solution = new_regulation.solution
    regulation.enabled = new_regulation.enabled
    regulation.key_words = new_regulation.key_words
    flask_db.session.commit()


def create_regulation_instance():
    return Regulation()


def add_regulation(regulation):
    flask_db.session.add(regulation)
    flask_db.session.commit()


def remove_regulation_by_id(regulation_id):
    regulation = Regulation.query.filter_by(id=regulation_id).first()
    flask_db.session.delete(regulation)
    flask_db.session.commit()
