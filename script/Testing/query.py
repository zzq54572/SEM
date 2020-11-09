import os
import xlrd
import sqlite3
import re





basedir='''C:\WorkSpace\PythonProgram\pycharm\SEM\datamart\SQLite'''
dbfile='''ssoetlmonitor.db'''
conn=sqlite3.connect(basedir+'\\'+dbfile)
table_name='task'
#rows=conn.execute(f"PRAGMA table_info({table_name})")
rows=conn.execute(f"select * from task ")
for row in rows:
    print(row)