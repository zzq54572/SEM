import os
controler_path=os.path.dirname(os.path.abspath(__file__))+"\\script\\Controler"

import sys
sys.path.append(controler_path)

from flask import Flask,render_template
from CrontabControler import *
from TlaControler import *
from EnvironmentControler import *
from ShiftWrapReportControler import *
from ComplianceReportControler import *
from HandoffControler import *
from TaskControler import *
from RegulationControler import *
from flaskapp import flask_app

@flask_app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    flask_app.run('127.0.0.1', debug=True, port=5000,
                  ssl_context=('./OpenSSL_crt/server.crt', './OpenSSL_crt/server.key'))
    # flask_app.run(debug=True)