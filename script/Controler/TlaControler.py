import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from TlaHandler import *
#from script.Controler.CommonControler import *
#from CommonHandler import *
from flask import render_template, url_for, redirect,request
from flaskapp import flask_app
from script.Form.forms import QueryForm,TlaForm
from script.Log.log import logging,log_stub,add_log_at_begin_and_end




@flask_app.route("/tla_query",methods=["GET","POST"])
def tla_query():
    tlas=GetTlaList()

    if request.method=='GET':
        result=request.args
        return render_template("./tla_query.html",tlas=tlas,rows=[])
        
    else:
        result=request.form
    
    #return render_template("show_request.html",result=result,method=request.method)    
    
    
    
    if "query" in result.keys():
        if "tla" in result.keys():
            tla=result["tla"].strip().upper()

        rows=query_tla_by_tla_unique(tla)
        return render_template("tla_query.html",tlas=tlas,rows=rows)

    elif "query_all" in result.keys():
        if "tla" in result.keys():
            tla=result["tla"].strip().upper().replace("*","%")
        if tla == "":
            tla = "%"
        rows=query_tla_by_tla(tla)
        return render_template("tla_query.html",tlas=tlas,rows=rows)


    elif "addnew" in result.keys():
        tla_form = TlaForm()
        row = create_tla_instance()
        return render_template("tla_update.html", row=row,opt="AddNew")
        #return redirect("tla_update.html", form=tla_form, row=row,opt="AddNew")

    elif "modify" in result.keys():
        row = create_tla_instance()
        #return render_template("show_request.html",result=result,method=request.method)
        row.id=result["id"]
        row.tla=result["tla"]
        row.customer_name=result["customer_name"]
        row.solution=result["solution"]
        row.tl=result["tl"]
        row.project_code=result["project_code"]
        row.runbook_url=result["runbook_url"]
        return render_template("tla_update.html", row=row,opt="Modify")

    elif "remove" in result.keys():
        row = create_tla_instance()
        #return render_template("show_request.html",result=result,method=request.method)
        row.id=result["id"]
        row.tla=result["tla"]
        row.customer_name=result["customer_name"]
        row.solution=result["solution"]
        row.tl=result["tl"]
        row.project_code=result["project_code"]
        row.runbook_url=result["runbook_url"]
        return render_template("tla_update.html",row=row,opt="Remove")
    else:
        return render_template("show_request.html", result=result, method=request.method)


@flask_app.route("/tla_update",methods=["GET","POST"])
def tla_update():
    tlas = GetTlaList()
    if request.method=='GET':
        result=request.args        
    else:
        result=request.form
    
     
    
    #row=create_tla_instance()

    if "modify_update" in result.keys():
        #return render_template("show_request.html",result=result,method=request.method)

        tla_id = result["id"].strip()
        row = query_tla_by_id(tla_id)
        row.tla=result["tla"].strip()
        row.customer_name=result["customer_name"].strip()
        row.solution=result["solution"].strip()
        row.tl=result["tl"].strip()
        row.project_code=result["project_code"].strip()
        row.runbook_url=result["runbook_url"].strip()
        
        update_tla(row)
        return render_template("tla_query.html",tlas=tlas,rows=[row])

    elif "addnew_update" in result.keys():
        # return render_template("show_request.html",result=result,method=request.method)
        row = create_tla_instance()
        row.tla = result["tla"].strip()
        row.customer_name = result["customer_name"].strip()
        row.solution = result["solution"].strip()
        row.tl = result["tl"].strip()
        row.project_code = result["project_code"].strip()
        row.runbook_url = result["runbook_url"].strip()

        add_tla(row)
        return render_template("tla_query.html", tlas=tlas, rows=[row])

    elif "remove_update" in result.keys():
        tla_id = result["id"].strip()
        print("remove tla", tla_id)
        remove_tla_by_id(tla_id)
        return render_template("tla_query.html", tlas=tlas,rows=[])

    elif "cancel" in result.keys():
        return render_template("tla_query.html", tlas=tlas,rows=[])

    else:
        return render_template("show_request.html", result=result, method=request.method)
        
        
