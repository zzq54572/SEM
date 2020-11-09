import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from CommonHandler import *

from database import *



from time import time, localtime
#from script.Log.log import *
from sqlalchemy import func

def create_environment_instance():
    return Environment()


def query_envrionment_all():
    all_environment = query_rows_all(Environment)
    return all_environment


def query_environment_by_tla(tla):
    # 使用ilike而不是like查询时的 username 字段就不会区分大小写了
    all_environment = Environment.query.filter(Environment.tla.ilike(f'%{tla}%')).all()
    return all_environment


def query_environment_unique(tla,deployment_type):
    all_tla_filter = Environment.query.filter(func.lower(Environment.tla) == func.lower(tla))
    all_environment=all_tla_filter.filter(func.lower(Environment.deployment_type) == func.lower(deployment_type)).all()
    return all_environment


def query_environment_by_id(id):
    environment = Environment.query.filter_by(id=id).first()
    return environment


def update_environment(new_environment):
    environment = Environment.query.filter_by(id=new_environment.id).first()
    environment.id = new_environment.id
    environment.tla = new_environment.tla
    environment.deployment_type = new_environment.deployment_type
    environment.server_type = new_environment.server_type
    environment.server_machine = new_environment.server_machine
    environment.terminal_machine = new_environment.terminal_machine
    environment.comment = new_environment.comment
    environment.monitored_by = new_environment.monitored_by
    environment.enabled = new_environment.enabled
    environment.key_words = new_environment.key_words
    environment.is_compliance = new_environment.is_compliance
    flask_db.session.commit()



def add_environment(environment):
    flask_db.session.add(environment)
    flask_db.session.commit()


def remove_environment_by_id(id):
    environment = Environment.query.filter_by(id=id).first()
    flask_db.session.delete(environment)
    flask_db.session.commit()
