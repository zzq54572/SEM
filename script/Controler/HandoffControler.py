import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from HandoffHandler import *
from flask import render_template, url_for, redirect,jsonify,request
from flaskapp import flask_app
from script.Form.forms import QueryForm,TlaForm
from script.Log.log import logging,log_stub,add_log_at_begin_and_end

#from script.Handler.CommonHandler import *


@flask_app.route("/handoff_create",methods=["GET","POST"])
def handoff_create():

    tlas= []
    # ["ACS","AMK","AMM","AMU","AMV","ANF","ASK","ASM","ASU","ASV","BLS","CSP","JCP","GDC","NSO"]
    tlas_principal=["AMK","AMM","AMU","AMV","ANF","JCP","NSO"]
    tlas_assitant=["ACS","ASK","ASM","ASU","ASV","BLS","CSP","GDC"]
    if request.method=='GET':
        #result=request.args
        return render_template("handoff.html", tlas=tlas_principal, owner="principal",handoff_to="Pune")
    else:
        form=request.form
        #return render_template("show_request.html", result=form, method=request.method)

        if "handoff_submit" not in form.keys():
            if form["owner"]=="principal":
                tlas=tlas_principal
            elif form["owner"]=="assistant":
                tlas=tlas_assitant
                # print("tlas:",tlas)
            else:
                tlas=tlas_principal+tlas_assitant
            # print(form["owner"])
            # print(tlas_assitant)
            # print(tlas_principal)
            # print(tlas)
            return render_template("handoff.html", tlas=tlas, owner=form["owner"],handoff_to=form["handoff_to"])
        else:
            #Config = InitConfig()
            DMJiras=Config["ActiveDMTickets"]

            handoff_time=GetReportTimeFlag()
            if handoff_time >= "9AM":
                handoff_comment_default=""" Hand off to """+ form["handoff_to"]+"."
            else:
                handoff_comment_default=""" Warm hand off to """+form["handoff_to"]+"."

            for tla, JiraTicketKey in DMJiras.items():
                print(tla,JiraTicketKey)
            #print(form)

            for tla,JiraTicketKey in DMJiras.items():
                tla = tla.upper()
                if tla in form.keys():
                    handoff_comment_custom=form[tla]
                    handoff_comment=handoff_comment_custom + "\n" + handoff_comment_default
                    #print(handoff_comment,JiraTicketKey)
                    AddComment(JiraTicketKey, handoff_comment)
            return render_template("handoff.html", tlas=tlas_principal, owner=form["owner"], handoff_to=form["handoff_to"])
    
@flask_app.route("/routineopt_comment",methods=["GET","POST"])
def routine_comment_submit():
    #Config = InitConfig()

    tlas=[]
    #print(Config.sections())
    for sec in Config.sections():
        #print(sec)
        if sec.find("RoutineOpt-")>=0:
            tlas.append(sec.strip()[-3:])
    #print(tlas)
    #JiraConn = GetJiraConnect(Config)
    if request.method=='GET':
        #result=request.args
        form={'tla':"NULL"}
        return render_template("routineopt_multisubmit.html", tlas=tlas, routineopts={},form=form)
    else:
        form=request.form
        #return render_template("show_request.html", result=form, method=request.method)

        if "routineopt_submit" in form.keys():

            DMJiras=Config["ActiveDMTickets"]
            JiraTicketKey=DMJiras[form["tla"]]
            handoff_comment=form["routineopt_comment"]
            if JiraTicketKey.strip() != "" or handoff_comment.strip() != "":
                #print(JiraTicketKey, handoff_comment)
                AddComment(JiraTicketKey, handoff_comment)
            return render_template("routineopt_multisubmit.html", tlas=tlas, routineopts={}, form=form)

        elif "routineopt_multi_submit" in form.keys():
            DMJiras = Config["ActiveDMTickets"]
            for key,value in form.items():
                if "dynamic_input_routine_tla_" in key:
                    key_tla=form[key].strip()
                    key_comment="dynamic_textarea_routine_comment_"+key.replace("dynamic_input_routine_tla_","")
                    JiraTicketKey = DMJiras[key_tla]
                    handoff_comment = form[key_comment]
                    if JiraTicketKey.strip() != "" and handoff_comment.strip() != "":
                        print(JiraTicketKey, handoff_comment)
                        AddComment(JiraTicketKey, handoff_comment)
            return render_template("routineopt_multisubmit.html", tlas=tlas, routineopts={}, form=form)

             #return render_template("show_request.html", result=form, method=request.method)

        else:
            if form["tla"] == "NULL":
                return render_template("routineopt_multisubmit.html", tlas=tlas, routineopts={}, form=form)

            # return render_template("show_request.html", result=form, method=request.method)
            RoutineOptSec = "RoutineOpt-" + form["tla"]
            print("OptSecTLA", RoutineOptSec)
            routineopts = Config[RoutineOptSec]
            # print(routineopts)
            # for key,value in items():
            #    routineopts[key]=value
            # for key, value in routineopts.items():
            #    print([key,'---',value])

            return render_template("routineopt_multisubmit.html", tlas=tlas, routineopts=routineopts, form=form)



        
@flask_app.route("/routine_refresh_opt",methods=["GET","POST"])
def routine_refresh_opt():
    tla=request.args.get('tla',"")
    #print("refresh tla:", tla)
    RoutineOptSec = "RoutineOpt-" + tla
    #print("OptSecTLA", RoutineOptSec)
    routineopts = Config[RoutineOptSec]
    result=''
    for key,val in routineopts.items():
        #print("jsonify:", result)
        if result=='':
            #print("jsonify 0beg:", result)
            result=result+ '\"'+key+'\":\"'+str(val)+'\"'
            #print("jsonify 0aft:", result)
        else:
            #print("jsonify 1beg:", result)
            result=result+',\"'+key+'\":\"'+str(val)+'\"'
            #print("jsonify: 1aft", result)
    result='{'+result+'}'

    return jsonify(result)
