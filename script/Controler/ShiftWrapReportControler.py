import os
handler_path=os.path.dirname(os.path.abspath(__file__))+"\\..\\Handler"

import sys
sys.path.append(handler_path)
from ShiftWrapReportHandler import *
from flask import render_template, url_for, redirect,request
from flaskapp import flask_app
from script.Form.forms import QueryForm,TlaForm
from script.Log.log import *
import datetime

import json
import os


@flask_app.route("/shiftwrap_report_view",methods=["GET","POST"])
def shiftwrap_report_view():
    if request.method == 'GET':

        html_content = createhtmlbody()
        report_name = "./templates/temp/shiftwrap_report_" + str(datetime.datetime.now())[0:19].replace(':', '-').replace(" ", "-") + ".html"
        # report_name="static/shiftwrap_report.html"
        html_file_standerby = open(report_name, "w+")
        print(html_content, file=html_file_standerby, flush=True)
        html_file_standerby.close()

        return render_template("shiftwrap_report_view.html")
    else:
        form = request.form
        if "send-inner" in form.keys():
            sendmail()

        elif "send-outer" in form.keys():
            sendmail("outer")

        return render_template("home.html")




@flask_app.route("/shiftwrap_report_create",methods=["GET","POST"])
def shiftwrap_report_create():
    all_reports=[report for report in os.listdir("./templates/temp/") if report.find("shiftwrap_report") >=0 and os.path.isdir(report) ==False]
    if len(all_reports)>0:
        newest_report=all_reports[0]

        for report in all_reports[1:]:
            if report > newest_report:
                os.remove("./templates/temp/" + newest_report)
                newest_report = report
            else:
                os.remove("./templates/temp/" + report)
        return render_template("./temp/" + newest_report)

    else:
        newest_report="No Data"
        return newest_report
