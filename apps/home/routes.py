# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request,jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from gui.database_interface import retrieve_contacts
from gui.database_interface import retrieve_data

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/components-forms.html', segment='dashboard')

@blueprint.post("/start")
@login_required 
def start():
    return jsonify({"message":"Running script now"})

@blueprint.route('/history')
@login_required 
def history():
    contacts = retrieve_contacts(web=True)
    print(contacts)
    return render_template("home/tables-bootstrap-tables.html",segment="Histroy", data=contacts)
def history():
    contacts = retrieve_contacts(web=True)
    print(contacts)
    return render_template("home/tables-bootstrap-tables.html",segment="Histroy", data=contacts)

@blueprint.route("/ajaxfile",methods=["POST","GET"])
@login_required
def ajaxfile():
    if request.method == 'POST':
        last_searched_date = request.form['userid']
        # print(last_searched_date)
        result = retrieve_data(last_searched_date)
        # print(employeelist)

    return jsonify({'htmlresponse': render_template('home/response.html', employeelist=result)})

@blueprint.route('/<template>')
# @login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
