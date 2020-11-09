import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from CommonHandler import *


#from script.Database.database import *
from time import time,localtime
#from script.Log.log import logging,log_stub,add_log_at_begin_and_end
from sqlalchemy import func
import re
import sqlite3
log=logging

   

        
@add_log_at_begin_and_end
def query_crontab_by_tla(tla,env,period_beg,period_end):
    tla=tla.upper()
    env=env.upper()


    all_crontabs=Crontab.query.filter(func.lower(Crontab.tla)==func.lower(tla)).filter(func.lower(Crontab.deployment_type)==func.lower(env)).all()
    crontabs=[]
    #if state=="all":
    #    crontabs = all_crontabs
    #else:
    #    if state=="next":
    #        offset_minute_start=0
    #        offset_minute_end=60*8
    #    elif state=="done":
    #        offset_minute_start=-60*8
    #        offset_minute_end=0
    #    else:
    #        offset_minute_start=-60*4
    #        offset_minute_end=60*4
    #
    if period_beg ==0 and period_end==0:
        crontabs=all_crontabs
    else:
        query_time_matrix = generate_query_time_matrix(period_beg, period_end)
        for crontab in all_crontabs:
            log(crontab)
            crontab_time_matrix=generate_crontab_time_matrix(crontab.minute,crontab.hour,crontab.day,crontab.month,crontab.wday)

                #is_crontab_valid=is_crontab_included(crontab.minute,crontab.hour,crontab.day,crontab.month,crontab.wday,offset_minute_start,offset_minute_end)
            is_crontab_valid=set(query_time_matrix).intersection(set(crontab_time_matrix))
            if is_crontab_valid:
               crontabs.append(crontab)
    
    return crontabs
        

       
def generate_crontab_time_matrix(crontab_minute,crontab_hour,crontab_day,crontab_month,crontab_wday):
    crontab_time_matrix=[]
    crontab_week_matrix =parse_crontab_time_section(crontab_wday,'week')
    crontab_month_matrix =parse_crontab_time_section(crontab_month,'month')
    crontab_day_matrix =parse_crontab_time_section(crontab_day,'day')
    crontab_hour_matrix =parse_crontab_time_section(crontab_hour,'hour')
    crontab_minute_matrix =parse_crontab_time_section(crontab_minute,'minute')
    
    if crontab_wday.strip()=="*" and ( crontab_month.strip() != "*" or crontab_day.strip() != "*" ):
        crontab_week_matrix=[]
    
    if crontab_wday.strip()!="*" and ( crontab_month.strip() == "*" or crontab_day.strip() == "*" ):
        crontab_month_matrix=[]
        crontab_day_matrix=[]
        
    for week in crontab_week_matrix:
        for hour in crontab_hour_matrix:
            for minute in crontab_minute_matrix:
                crontab_time_matrix.append((week,hour,minute))
    
    for month in crontab_month_matrix:
        for day in crontab_day_matrix:
            for hour in crontab_hour_matrix:
                for minute in crontab_minute_matrix:
                    crontab_time_matrix.append((month,day,hour,minute))
    
    
    
    return crontab_time_matrix
 
def parse_crontab_time_section(crontab_time_section,section_type):
    section_min=0
    section_max=0
    full_time_points=[]
    
    crontab_time_section=crontab_time_section.upper()
    section_type =section_type.upper()
    if section_type=="WEEK":
        crontab_time_section=crontab_time_section.replace('MON','1')
        crontab_time_section=crontab_time_section.replace('TUE','2')
        crontab_time_section=crontab_time_section.replace('WED','3')
        crontab_time_section=crontab_time_section.replace('THU','4')
        crontab_time_section=crontab_time_section.replace('FRI','5')
        crontab_time_section=crontab_time_section.replace('SAT','6')
        crontab_time_section=crontab_time_section.replace('SUN','0')
        crontab_time_section=crontab_time_section.replace('7','0')
        section_min=0
        section_max=6
    elif section_type=="MONTH":
        section_min=1
        section_max=12
    elif section_type=="DAY":
        section_min=1
        section_max=31
    elif section_type=="HOUR":
        section_min=0
        section_max=23
    elif section_type=="MINUTE":
        section_min=0
        section_max=59
    else:
        pass
    
    time_points=crontab_time_section.split(',')
    
    for point in time_points:
        point=point.strip()
        if '/' in point:
            sub_points=point.split('/')
            if '*' == sub_points[0]:
                sub_points[0]=0
            full_time_points+=range(int(sub_points[0]),section_max,int(sub_points[1]))
        elif '-' in point:
            sub_points=point.split('-')
            full_time_points+=range(int(sub_points[0]),int(sub_points[1])+1 )
        elif '*' == point:
            full_time_points+=range(section_min,section_max+1 )
        else:
            #point = int(point)
            #print("convert point:", point)
            #full_time_points.append(point)
            try:
                point=int(point)
                print("convert point:",point)
                full_time_points.append(point)
            except:
                print("type:",section_type,"point:",point)
                print(full_time_points)
                exit(-1)
    return full_time_points


def generate_query_time_matrix(offset_minute_start, offset_minute_end):
    query_time_matrix = []
    query_time_begin = int(time() - offset_minute_start * 60)
    query_time_end = int(time() + offset_minute_end * 60)
    query_time_range = range(query_time_begin, query_time_end + 1, 60)

    for tm in query_time_range:
        local_tm = localtime(tm)
        query_time_matrix.append(((local_tm.tm_wday + 1) % 7, local_tm.tm_hour, local_tm.tm_min))
        query_time_matrix.append((local_tm.tm_mon, local_tm.tm_mday, local_tm.tm_hour, local_tm.tm_min))
    return query_time_matrix


def reload_crontab_file(tla,env, crontab_items):
    tla=tla.upper()
    env=env.upper()
#    #basedir = '''C:\WorkSpace\PythonProgram\pycharm\SEM\datamart\SQLite'''
    #dbfile = '''ssoetlmonitor.db'''
#
    #conn = sqlite3.connect(basedir + '\\' + dbfile)
    #delete_sql=f'delete from crontab where tla="{tla}" and deployment_type="{env}"'
    #conn.execute(delete_sql)
    #conn.commit()
    #o=flask_db.session.query(Crontab).filter(func.lower(Crontab.tla) == func.lower(tla)).filter(func.lower(Crontab.deployment_type) == func.lower(env)).delete(synchronize_session="fetch")
    #flask_db.session.commit()
    #print("clear:",str(o))
    old_crontabs=Crontab.query.filter(func.lower(Crontab.tla)==func.lower(tla)).filter(func.lower(Crontab.deployment_type)==func.lower(env)).all()
    for item in old_crontabs:
        flask_db.session.delete(item)
        flask_db.session.commit()
        print("delete:",item)

    new_crontab_content=""
    for item in crontab_items:
        #item=item.decode("utf-8")
        item=item.strip()
        item_splits = re.split(r"\s+", item.replace("\"","%"))
        # print(cron)
        schedule = ''.join(item_splits[5:])
        new_crontab = Crontab()
        new_crontab.tla = tla
        new_crontab.deployment_type =env
        new_crontab.minute = item_splits[0]
        new_crontab.hour = item_splits[1]
        new_crontab.day = item_splits[2]
        new_crontab.month = item_splits[3]
        new_crontab.wday = item_splits[4]
        new_crontab.command = schedule
        new_crontab.enabled = "enabled"

        new_crontab_content=new_crontab_content+"\n"+str(new_crontab)
        flask_db.session.add(new_crontab)
        flask_db.session.commit()
        print("add :", new_crontab)

    new_crontabs = Crontab.query.filter(func.lower(Crontab.tla) == func.lower(tla)).filter(
        func.lower(Crontab.deployment_type) == func.lower(env)).all()
    #for item in new_crontabs:
    #    print("new:", item)
    return new_crontab_content
