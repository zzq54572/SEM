import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from CommonHandler import *

from database import *



from time import time, localtime
#from script.Log.log import *
from sqlalchemy import func




def query_tla_all():
    all_tla = query_rows_all(Tla)
    return all_tla


def query_tla_by_tla(tla):
    # 使用ilike而不是like查询时的 username 字段就不会区分大小写了
    all_tla = Tla.query.filter(Tla.tla.ilike(f'%{tla}%')).all()
    return all_tla


def query_tla_by_tla_unique(tla):
    all_tla = Tla.query.filter(func.lower(Tla.tla) == func.lower(tla)).all()
    return all_tla


def query_tla_by_id(id):
    tla = Tla.query.filter_by(id=id).first()
    return tla


def update_tla(new_tla):
    tla = Tla.query.filter_by(id=new_tla.id).first()
    print("update tla:", type(tla), tla)
    tla.tla = new_tla.tla
    tla.customer_name = new_tla.customer_name
    tla.solution = new_tla.solution
    tla.tl = new_tla.tl
    tla.project_code = new_tla.project_code
    tla.runbook_url = new_tla.runbook_url
    flask_db.session.commit()


def create_tla_instance():
    return Tla()


def add_tla(tla):
    print("add tla:", type(tla), tla)

    flask_db.session.add(tla)
    flask_db.session.commit()


def remove_tla_by_id(tla_id):
    tla_row = Tla.query.filter_by(id=tla_id).first()
    print("remove tla:", type(tla_row), tla_row)
    flask_db.session.delete(tla_row)
    flask_db.session.commit()
