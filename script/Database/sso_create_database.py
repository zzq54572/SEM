#!/usr/bin/env python
# coding: utf-8

# In[1]:


################
###创建数据库####
###############
import sqlite3

conn=sqlite3.connect('''C:\WorkSpace\PythonProgram\SSOETLMonitor\ssoetlmonitor.db''')

###调度作业###
conn.execute('''create table crontab (
             tla text,
             minute text,
             hour text,
             day text,
             month text,
             wday text,
             command text, 
             crontab text, 
             enabled integer, 
             key_words text)''')
###操作条例###
conn.execute('''create table regulation(
                tla text, 
                reporter text, 
                begin_time text, 
                description text,
                enabled integer, 
                key_words text)''')


###工作任务###
conn.execute('''create table task(
                tla text, 
                ticket_type text, 
                ticket_number text,
                begin_time text,
                description text,
                enabled integer, 
                key_words text)''')

###问题错误###
conn.execute('''create table issue(
                tla text, 
                ticket_type text, 
                ticket_number text,
                begin_time text,
                description text,
                enabled integer, 
                key_words text)''')

conn.close()


# In[ ]:




