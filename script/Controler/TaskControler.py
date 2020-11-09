import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from TaskHandler import *
from ComplianceReportHandler2 import *
from flask import render_template, url_for, redirect,request
from flaskapp import flask_app
from script.Form.forms import QueryForm,TlaForm




@flask_app.route("/task_query",methods=["GET","POST"])
def task_query():

    if request.method=='GET':
        result=request.args
        return render_template("./task_query.html",jiras=[],tasks=[])
        
    else:
        result=request.form
    
    #return render_template("show_request.html",result=result,method=request.method)    
    
    
    
    if "refresh" in result.keys():
        if "taskdays" in result.keys():
            jirafilterurl=result["taskdays"].strip()+"ticketfilterurl"
            print(jirafilterurl)
            jira_tickets = GetJiraTickets(jirafilterurl)
            #print(jira_tickets)
            tasks=query_all_task()
            taskslist=[]
            for task in tasks:
                taskslist.append(task.tla+": "+task.description)
            #for jira in jira_tickets:
            #    task=create_task_instance()
            #    task.tla = jira["issuekey"]
            #    task.description=jira["summary"]
            #    tasks.append(task)
            #print(tasks)
        return render_template("task_query.html",jiras=jira_tickets,tasks=tasks)
    elif "done" in result.keys():
        if "tla" in result.keys():
            tla=result["tla"].strip().upper().replace("*","%")
        if tla == "":
            tla = "%"
        rows=query_tla_by_tla(tla)
        return render_template("tla_query.html", rows=rows)


    elif "addnew" in result.keys():
        row = create_task_instance()
        return render_template("task_update.html", row=row,opt="AddNew")
        #return redirect("tla_update.html", form=tla_form, row=row,opt="AddNew")

    elif "modify" in result.keys():
        row = create_task_instance()
        #return render_template("show_request.html",result=result,method=request.method)
        row.tla = result["tla"]
        row.env = result["env"]
        row.assigner = result["assigner"]
        row.lev = result["lev"]
        row.ticket_type = result["ticket_type"]
        row.ticket_number = result["ticket_number"]
        row.begin_time = result["begin_time"]
        row.end_time = result["end_time"]
        row.description = result["description"]
        row.enabled = result["enabled"]
        row.key_words = result["key_words"]
        return render_template("task_update.html", row=row,opt="Modify")

    elif "remove" in result.keys():
        row = create_task_instance()
        #return render_template("show_request.html",result=result,method=request.method)
        row.id=result["id"]
        row.tla = result["tla"]
        row.env = result["env"]
        row.assigner = result["assigner"]
        row.lev = result["lev"]
        row.ticket_type = result["ticket_type"]
        row.ticket_number = result["ticket_number"]
        row.begin_time = result["begin_time"]
        row.end_time = result["end_time"]
        row.description = result["description"]
        row.enabled = result["enabled"]
        row.key_words = result["key_words"]
        return render_template("task_update.html",row=row,opt="Remove")
    else:
        return render_template("show_request.html", result=result, method=request.method)


@flask_app.route("/task_update",methods=["GET","POST"])
def task_update():
    tlas = GetTlaList()
    if request.method=='GET':
        result=request.args        
    else:
        result=request.form
    
     
    
    #row=create_tla_instance()

    if "modify_update" in result.keys():
        #return render_template("show_request.html",result=result,method=request.method)

        task_id = result["id"].strip()
        row = query_task_by_id(task_id)

        row.tla = result["tla"]
        row.env = result["env"]
        row.assigner = result["assigner"]
        row.lev = result["lev"]
        row.ticket_type = result["ticket_type"]
        row.ticket_number = result["ticket_number"]
        row.begin_time = result["begin_time"]
        row.end_time = result["end_time"]
        row.description = result["description"]
        row.enabled = result["enabled"]
        row.key_words = result["key_words"]
        
        update_task(row)
        return render_template("task_query.html",tlas=tlas,rows=[row])

    elif "addnew_update" in result.keys():
        # return render_template("show_request.html",result=result,method=request.method)
        row = create_task_instance()
        row.tla = result["tla"]
        row.env = result["env"]
        row.assigner = result["assigner"]
        row.lev = result["lev"]
        row.ticket_type = result["ticket_type"]
        row.ticket_number = result["ticket_number"]
        row.begin_time = result["begin_time"]
        row.end_time = result["end_time"]
        row.description = result["description"]
        row.enabled = result["enabled"]
        if result["enabled"].strip() =="":
            row.enabled="Y"

        row.key_words = result["key_words"]

        add_task(row)
        return render_template("task_query.html", tlas=tlas, rows=[row])

    elif "remove_update" in result.keys():
        task_id = result["id"].strip()
        remove_task_by_id(task_id)
        return render_template("task_query.html", tlas=tlas,rows=[])

    elif "cancel" in result.keys():
        return render_template("task_query.html", tlas=tlas,rows=[])

    else:
        return render_template("show_request.html", result=result, method=request.method)
        
        
