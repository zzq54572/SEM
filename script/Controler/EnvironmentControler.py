import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from EnvironmentHandler import *

#from script.Controler.CommonControler import *
#from CommonHandler import *
from flask import render_template, url_for, redirect,request
from flaskapp import flask_app
from script.Form.forms import QueryForm,TlaForm
from script.Log.log import logging,log_stub,add_log_at_begin_and_end




@flask_app.route("/environment_query",methods=["GET","POST"])
def environment_query():
    tlas=GetTlaList()

    if request.method=='GET':
        result=request.args
        return render_template("./environment_query.html",tlas=tlas,rows=[])
        
    else:
        result=request.form
    
    #return render_template("show_request.html",result=result,method=request.method)    
    
    
    
    if "query" in result.keys():
        if "tla" in result.keys() and "deployment_type" in result.keys():
            tla=result["tla"].strip().upper()
            deployment_type=result["deployment_type"].strip().upper()
            rows=query_environment_unique(tla,deployment_type)

        else:
            rows=[]
        return render_template("environment_query.html", tlas=tlas, rows=rows)
    elif "query_all" in result.keys():
        if "tla" in result.keys():
            tla=result["tla"].strip().upper().replace("*","%")
        if tla == "":
            tla = "%"
        rows=query_environment_by_tla(tla)
        return render_template("environment_query.html",tlas=tlas,rows=rows)


    elif "addnew" in result.keys():
        row = create_environment_instance()
        return render_template("environment_query.html", row=row,opt="AddNew")
        #return redirect("tla_update.html", form=tla_form, row=row,opt="AddNew")

    elif "modify" in result.keys() or "remove" in result.keys():
        row = create_environment_instance()
        #return render_template("show_request.html",result=result,method=request.method)
        row.id = result["id"]
        row.tla = result["tla"]
        row.deployment_type = result["deployment_type"]
        row.server_type = result["server_type"]
        row.server_machine = result["server_machine"]
        row.terminal_machine = result["terminal_machine"]
        row.comment = result["comment"]
        row.monitored_by = result["monitored_by"]
        row.enabled = result["enabled"]
        row.key_words = result["key_words"]
        row.is_compliance = result["is_compliance"]

        if "modify" in result.keys():
            opt="Modify"

        if "remove" in result.keys():
            opt="Remove"

        return render_template("environment_update.html", row=row,opt=opt)

    else:
        return render_template("show_request.html", result=result, method=request.method)


@flask_app.route("/environment_update",methods=["GET","POST"])
def environment_update():
    tlas = GetTlaList()
    if request.method=='GET':
        result=request.args        
    else:
        result=request.form


    if "modify_update" in result.keys() or "addnew_update" in result.keys():

        #return render_template("show_request.html",result=result,method=request.method)
        if "modify_update" in result.keys():
            environment_id = result["id"].strip()
            row = query_environment_by_id(environment_id)

        if "addnew_update" in result.keys():
            row = create_tla_instance()

        row.tla = result["tla"]
        row.deployment_type = result["deployment_type"]
        row.server_type = result["server_type"]
        row.server_machine = result["server_machine"]
        row.terminal_machine = result["terminal_machine"]
        row.comment = result["comment"]
        row.monitored_by = result["monitored_by"]
        row.enabled = result["enabled"]
        row.key_words = result["key_words"]
        row.is_compliance = result["is_compliance"]

        if "modify_update" in result.keys():
            update_environment(row)
        if "addnew_update" in result.keys():
            add_environment(row)

        return render_template("environment_query.html",tlas=tlas,rows=[row])

    elif "remove_update" in result.keys():
        environment_id = result["id"].strip()
        remove_environment_by_id(environment_id)
        return render_template("environment_query.html", tlas=tlas,rows=[])

    elif "cancel" in result.keys():
        return render_template("environment_query.html", tlas=tlas,rows=[])

    else:
        return render_template("show_request.html", result=result, method=request.method)
        
        
