import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from CommonHandler import *

from database import *



from time import time, localtime
#from script.Log.log import *
from sqlalchemy import func


def create_task_instance():
    return Task()

def query_all_task():
    tasks=Task.query.all()
    return tasks

def query_active_tasks():
    tasks=Task.query.filter(func.lower(Task.enabled) == 'y').all()
    return tasks

def query_task_by_tla(tla):
    # 使用ilike而不是like查询时的 username 字段就不会区分大小写了
    all_task = Task.query.filter(Task.tla.ilike(f'%{tla}%')).all()
    return all_task


def query_task_by_id(id):
    task = Task.query.filter_by(id=id).first()
    return task


def update_task(new_task):
    task = Task.query.filter_by(id=new_task.id).first()
    task.tla = new_task.tla
    task.env = new_task.env
    task.assigner = new_task.assigner
    task.lev = new_task.lev
    task.ticket_type = new_task.ticket_type
    task.ticket_number = new_task.ticket_number
    task.begin_time = new_task.begin_time
    task.end_time = new_task.end_time
    task.description = new_task.description
    task.enabled = new_task.enabled
    task.key_words = new_task.key_words
flask_db.session.commit()





def add_task(task):
    flask_db.session.add(task)
    flask_db.session.commit()


def remove_task_by_id(task_id):
    task_row = Task.query.filter_by(id=task_id).first()
    flask_db.session.delete(task_row)
    flask_db.session.commit()
