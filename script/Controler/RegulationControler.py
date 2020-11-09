import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from RegulationHandler import *
from flask import render_template, url_for, redirect,request
from flaskapp import flask_app




@flask_app.route("/regulation_query",methods=["GET","POST"])
def regulation_query():
    tlas=GetTlaList()
    if request.method=='GET':
        result=request.args
        return render_template("./regulation_query.html",tlas=tlas,rows=[])
        
    else:
        result=request.form
    
    #return render_template("show_request.html",result=result,method=request.method)    
    
    
    
    if "query" in result.keys():
        if "tla" in result.keys():
            tla=result["tla"].strip().upper()

        rows=query_regulation_by_tla_unique(tla)
        return render_template("regulation_query.html",tlas=tlas,rows=rows)

    elif "query_all" in result.keys():
        if "tla" in result.keys():
            tla=result["tla"].strip().upper().replace("*","%")
        if tla == "":
            tla = "%"
        rows=query_regulation_by_tla(tla)
        return render_template("regulation_query.html",tlas=tlas,rows=rows)


    elif "addnew" in result.keys():
        row = create_regulation_instance()
        return render_template("regulation_update.html", row=row,opt="AddNew")
        #return redirect("tla_update.html", form=tla_form, row=row,opt="AddNew")

    elif "modify" in result.keys():
        row = create_regulation_instance()
        row.id = result["id"]
        row.tla = result["tla"]
        row.reporter = result["reporter"]
        row.begin_time = result["begin_time"]
        row.end_time = result["end_time"]
        row.summary = result["summary"]
        row.description = result["description"]
        row.solution = result["solution"]
        row.enabled = result["enabled"]
        row.key_words = result["key_words"]
        return render_template("regulation_update.html", row=row,opt="Modify")

    elif "remove" in result.keys():
        row = create_regulation_instance()
        row.id = result["id"]
        row.tla = result["tla"]
        row.reporter = result["reporter"]
        row.begin_time = result["begin_time"]
        row.end_time = result["end_time"]
        row.summary = result["summary"]
        row.description = result["description"]
        row.solution = result["solution"]
        row.enabled = result["enabled"]
        row.key_words = result["key_words"]
        return render_template("regulation_update.html",row=row,opt="Remove")
    else:
        return render_template("show_request.html", result=result, method=request.method)


@flask_app.route("/regulation_update",methods=["GET","POST"])
def regulation_update():
    tlas = GetTlaList()
    if request.method=='GET':
        result=request.args        
    else:
        result=request.form
    
     
    
    #row=create_tla_instance()

    if "modify_update" in result.keys():
        #return render_template("show_request.html",result=result,method=request.method)
        regulation_id = result["id"].strip()
        row = query_regulation_by_id(regulation_id)
        row.tla = result["tla"].strip()
        row.reporter = result["reporter"].strip()
        row.begin_time = result["begin_time"].strip()
        row.end_time = result["end_time"].strip()
        row.summary = result["summary"].strip()
        row.description = result["description"].strip()
        row.solution = result["solution"].strip()
        row.enabled = result["enabled"].strip()
        row.key_words = result["key_words"].strip()
        update_regulation(row)
        return render_template("regulation_query.html",tlas=tlas,rows=[row])

    elif "addnew_update" in result.keys():

        row = create_regulation_instance()
        row.tla = result["tla"].strip()
        row.reporter = result["reporter"].strip()
        row.begin_time = result["begin_time"].strip()
        row.end_time = result["end_time"].strip()
        row.summary = result["summary"].strip()
        row.description = result["description"].strip()
        row.solution = result["solution"].strip()
        row.enabled = result["enabled"].strip()
        row.key_words = result["key_words"].strip()
        add_regulation(row)
        return render_template("regulation_query.html", tlas=tlas, rows=[row])

    elif "remove_update" in result.keys():
        regulation_id = result["id"].strip()
        remove_regulation_by_id(regulation_id)
        return render_template("regulation_query.html", tlas=tlas,rows=[])

    elif "cancel" in result.keys():
        return render_template("regulation_query.html", tlas=tlas,rows=[])

    else:
        return render_template("show_request.html", result=result, method=request.method)
        
@flask_app.route("/regulation_view",methods=["GET","POST"])
def regulation_view():
    tlas = GetTlaList()
    if request.method == 'GET':
        result=request.args

    else:
        result = request.form
    if result.get("cancel",0)==0:
        regulation_id = result["id"].strip()
        regulation=query_regulation_by_id(regulation_id)
        return render_template("regulation_view.html", row=regulation)
    else:
        tlas = GetTlaList()
        return render_template("regulation_query.html",tlas=tlas,row=[])

