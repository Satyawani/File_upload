# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
License: MIT
"""

import os
import logging
import json
from datetime import datetime
from dbasefile import *
# import Flask
from flask import Flask, render_template, send_from_directory, request, flash, redirect, Response

from util import csv_to_json, list_csv_files, get_tail, get_date_ms


# Inject Flask magic
app = Flask(__name__, static_folder="static")

# Config
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'Super_s3cret777'


# Default Route
@app.route('/')
def index():

    return render_template('index.html', segment='index.html')


@app.route('/sign_out')
def sign_out():

    message = "assets/img/inventory.png"
    return render_template('sign-in.html', message=message)

# convert_file


@app.route("/getcovert_fun")
def getcovert_fun():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    # convert_supp_item_count('samples\data.csv')
    return render_template('convert_datatable.html', segment = 'convert_datatable.html')

# Data Tables pages


@app.route('/datatables/', methods=['GET', 'POST'])
def datatables():

    # Page data used in POST & GET
    msg = ''
    input = ''
    csv_files = []

    for f in list_csv_files('samples'):
        csv_files.append(get_tail(f))

    if request.method == 'POST':
        if 'file' not in request.files:
            msg = 'No file part'
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            msg = 'No file'
            return redirect(request.url)

        if file:

            filename = file.filename.replace(
                '.csv', '_' + get_date_ms() + '.csv')
            print(filename)
            filename_1 = filename
            filename = 'data.csv'
            file.save(os.path.join('samples', filename))
            print(os.path.join('samples', filename))
            file_with_supp_item(os.path.join('samples', filename))

            msg = 'File saved: ' + filename_1

            csv_files.append(filename)

    else:

        input = request.args.get('input')

        if not input:
            input = 'data.csv'

    return render_template('datatables.html', input=input, csv_files=csv_files, msg=msg)

# Data Tables pages


@app.route('/api/from_csv')
def load_csv():

    input = request.args.get('input')

    if not input:
        input = 'data.csv'

    aPath = os.path.join(app.root_path, 'samples', input)
    data = csv_to_json(aPath)
    # print(data)

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response

# Data Tables pages


@app.route('/api/from_json')
def load_json():
    return send_from_directory(os.path.join(app.root_path, 'samples'), 'data.json')

# Download_file


@app.route("/getPlotCSV")
def getPlotCSV():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    csv = open('requirements.txt')
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})


# For Python Bootstrap
if __name__ == "__main__":
    app.run()
