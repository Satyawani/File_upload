# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
License: MIT
"""
import ast
import os
import logging
import ast
import json
import shutil
from datetime import *
from dbasefile import *
# import Flask
from flask import Flask, render_template, send_from_directory, request, flash, redirect, Response,jsonify,url_for,session
import requests
from util import csv_to_json, list_csv_files, get_tail, get_date_ms


# Inject Flask magic
app = Flask(__name__, static_folder="static")

# Config
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'Super_s3cret777'

import re

# Function to check if a string contains special characters
def contains_special_characters(text):
    # Define a regular expression to match special characters
    special_characters_pattern = re.compile(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\]')

    # Search for special characters in the text
    return bool(special_characters_pattern.search(text))

# Function to check if a DataFrame contains special characters
def dataframe_contains_special_characters(df):
    for column in df.columns:
        for cell in df[column]:
            if isinstance(cell, str) and contains_special_characters(cell):
                return True
    return False




# Default Route
@app.route('/')
def index():

    message = "static/assets/img/inventory.png"
    # print(os.getcwd())
    # # os.chdir("samples/")
    # print(os.listdir())
    # for i in os.listdir():
    #     os.remove(i)

    path = "samples/"
    shutil.rmtree(path)
    os.mkdir("samples/")
    # os.chdir("File_upload")
    return render_template('sign-in.html', message=message)



#Implemented multiselect concept fetch multi data
@app.route('/adim', methods=['POST', 'GET'])
def admin12():
    if request.method == 'POST':
        print("hello")
        cn, cur = dbfun()
        global uname
        uname = request.form.get('username')
        passw = request.form.get('passwd')
        print(uname, passw)
        print(f"select * from user_mst where c_user_id='{uname}' and c_user_pass='{passw}' ")
        cur.execute(f"select * from user_mst where c_user_id='{uname}' and c_user_pass='{passw}' ")
        b=cur.fetchall()
        print('count',len(b))
        if len(b) == 1:
            session['username'] = uname
            return render_template('datatables.html')
        else:
            return render_template('sign-in.html')



@app.route('/sign_out')
def sign_out():

    message = "assets/img/inventory.png"
    path = "samples/"
    shutil.rmtree(path)
    os.mkdir("samples/")
    # print(os.listdir())
    # for i in os.listdir():
    #     os.remove(i)
    return render_template('sign-in.html', message=message)

# convert_file

@app.route("/getconvert_fun" ,methods=['GET'])
def getconvert_fun():
    print('convert_screen',session['username'])
    input = request.form.get('file')
    # print(input)
    # print(type(input),f"samples/".join({str(input)}))
    #
    df=pd.read_csv(rf"samples/data.csv")
    # df=pd.read_csv(rf"data.csv")

    df=convert_supp_item_count(df)

    data=df.to_dict('records')
    # print('file',data)
    # print(data)
    # data = request.args.to_dict()
    # print(jsonify(data))

    # return redirect(url_for('result', data=data))
    return render_template('convert_datatable.html', data=data)


@app.route('/result/<data>')
def result():
    data = request.args.getlist('data')
    # print('edf',data)
    data= [ast.literal_eval(data[0])]
    # print('3ada',data)
    return render_template('convert_datatable.html', data=data)



@app.route('/history_log')
def history_log():
    cn,cur=dbfun()

    df = pd.read_sql("select d_date,c_br_code,c_supp_code,c_supplier_name,n_item_count,n_rate_sum,c_purchase_order_no,c_status,c_message from central_purchase_order order by d_date desc",cn)
    cn.close()


    data = df.to_dict('records')
    return render_template('log_file_screen.html', data=data)


# Data Tables pages
@app.route('/datatables/', methods=['POST', 'GET'])
def datatables():
    # os.chdir(r"E:\New folder (2)\File_upload")

    # Page data used in POST & GET
    msg = ''
    input = ''
    csv_files = []


    for f in list_csv_files('samples'):
        csv_files.append(get_tail(f))

    if request.method == 'POST':
        print("filesrequest",request.files)


        if 'file' not in request.files:
            msg = 'No file part'
            print(msg)
            return redirect(request.url)

        file = request.files['file']
        print(file,'dsad')
        if file.filename == '':
            msg = 'No file'
            return redirect(request.url)

        if file:



            filename = file.filename.replace(
                '.csv', '_' + get_date_ms() + '.csv')
            print(filename)
            filename_1 = filename
            filename = 'data.csv'
            print(os.path)
            print("location", os.path.join('samples', filename))
            file.save( os.path.join('samples', filename))




            df=file_with_supp_item(filename)
            if df.shape[0]!=0:



                msg = 'File saved: ' + filename_1

                csv_files.append(filename)
            else:
                pass
                # raise  Exception("Invaild data")

    else:

        input = request.args.get('input')

        if not input:

            # input=''
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
    # data = csv_to_json(input)
    print(data)

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
    csv = open(r'order_template.csv')
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=Order_Template_data.csv"})


@app.route('/postingendpoint', methods=['POST'])
def endpoint():
    try:
        item_id = request.form.get('rowData')
        item_id=ast.literal_eval(item_id)
        a=[]
        # print(item_id)
        # print(type(item_id['item_Details']),item_id['item_Details'])
        for i in range(0,len(item_id['item_Details'])):


            full_len={'itemcode':str(item_id['item_Details'][i]),'qty':str(item_id['qty_value'][i]),'rate':str(item_id['rate_Details'][i])}
            a.append(full_len)

        json_list={
            "cindex": "insert",
            "suppcode": f"{item_id['supplier_code']}",
            "c_ref_br_code": f"{item_id['br_code']}",
            "total":f"{item_id['total_sum']}"

        }
        json_list['itemlist']=a

        # print(json_list)
        headers = {'Content-type': 'application/json'}

        # res_1=requests.post(post_url+json.dumps(json_list), timeout=2.50)
        # print(res_1)
        # res_1={'code': '400', 'Status': 'Success', 'Message': 'Order Created Successfully', 'PurchaseOrderNo': '503/23/O/10295'}
        #
        res_1 = requests.post(post_url+json.dumps(json_list), timeout=2.50, headers=headers)
        # print(res_1.json())
        # a = json.dumps({'code': '200', 'Status': 'Success', 'Message': 'Order Created Successfully', 'PurchaseOrderNo': '503/23/O/15516'})

        a =res_1.json()


        try:
            print(a['PurchaseOrderNo'])
            cn,cur=dbfun()
            item_id['PurchaseOrderNo']=a['PurchaseOrderNo']
            item_id['Status'] = a['Status']
            item_id['Message'] = a['Message']
            item_id['Date']=str(date.today())
            del item_id['rate_sum']
            del item_id['sr_no']
            del item_id['Purchase_Order_no']
            # print(item_id)
            datafile=item_id.values()

            final_data_value=[]
            for i in datafile:
                final_data_value.append(str(i))

            # print('values',final_data_value)

            query = "INSERT INTO central_purchase_order(c_br_code,n_item_count,item_Details,n_pack_qty,qty_value,rate_Details,c_supp_code,c_supplier_name,n_rate_sum,c_purchase_order_no,c_status,c_message,d_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # print(query, final_data_value)
            fet=cur.execute(query,final_data_value)
            # print(fet)
            cn.commit()
            cn.close()
        except Exception as e:
            print(e)
        # a={'code': '200', 'Status': 'Success', 'Message': 'Order Created Successfully', 'PurchaseOrderNo': '503/23/O/15326'}
        a=json.dumps(res_1.json())
        # print("Testing",json.dumps(a))
        # Perform actions based on the item_id received
        # Example: make database updates, trigger other processes, etc.
        # return res_1.json()
        return a
    except Exception as e:


        return jsonify({'error': str(e)}), 500


# @app.route('/insert-into-database', methods=['POST'])
# def insert_into_database():
#     try:
#         request_data = request.get_json()
#         response_data = json.loads(request_data['response'])
#
#         # Perform the database insertion using response_data
#         # ... Your database insertion logic ...
#
#         # Return a response indicating success
#         return jsonify({'message': 'Data inserted into the database successfully'})
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

def process_selected_rows(selected_rows):
    # Placeholder logic to illustrate updating data
    updated_data = []
    # print(selected_rows,type(selected_rows))


    selected_rows = ast.literal_eval(selected_rows)

    for item_id in selected_rows:
        # print(selected_rows,type(selected_rows))

        # item_id = ast.literal_eval(row)
        # print(item_id['rowData'])
        # item_id=item_id['rowData']
        a = []

        for i in range(0, len(item_id['item_Details'])):
            full_len={'itemcode':str(item_id['item_Details'][i]),'qty':str(item_id['qty_value'][i]),'rate':str(item_id['rate_Details'][i])}
            a.append(full_len)

        json_list = {
            "cindex": "insert",
            "suppcode": f"{item_id['supplier_code']}",
            "c_ref_br_code": f"{item_id['br_code']}",
            "total": f"{round(item_id['total_sum'],2)}"

        }
        json_list['itemlist'] = a

        # print('edr',json_list)
        headers = {'Content-type': 'application/json'}
        # print(post_url + json.dumps(json_list))

        res_1 = requests.post(post_url + json.dumps(json_list), timeout=2.50, headers=headers)
        # print(res_1.json())
        # a=json.loads(res_1.json())
        # print(res_1.json(),type(res_1.json()))

        res_1=res_1.json()
        if res_1['code']=='200':
        # Update posting details and create an updated row
            updated_row = {
                # 'purchase_no': row['purchase_no'],  # Assuming this key exists in row data
                'sr_no':item_id['sr_no'],
                'Purchase_Order_no':res_1['PurchaseOrderNo']
                # Add other fields as needed
            }
        else:
            updated_row = {
                # 'purchase_no': row['purchase_no'],  # Assuming this key exists in row data
                'sr_no': item_id['sr_no'],
                'Purchase_Order_no': res_1['Message']
                # Add other fields as needed
            }

        # print(updated_row)

        updated_data.append(updated_row)
        try:
            # print(res_1['PurchaseOrderNo'])
            cn,cur=dbfun()
            item_id['Purchase_Order_no']=res_1['PurchaseOrderNo']
            item_id['Status'] = res_1['Status']
            item_id['Message'] = res_1['Message']
            item_id['Date'] = str(date.today())
            del item_id['rate_sum']
            del item_id['sr_no']
            # print(item_id)
            datafile=item_id.values()
            # print(datafile)

            final_data_value=[]
            for i in datafile:
                final_data_value.append(str(i))

            # print('data',final_data_value)

            query = "INSERT INTO central_purchase_order(c_purchase_order_no,c_br_code,n_item_count,item_Details,n_pack_qty,qty_value,rate_Details,c_supp_code,c_supplier_name,n_rate_sum,c_status,c_message,d_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # print(query, final_data_value)
            fet=cur.execute(query,final_data_value)
            # print(fet)
            cn.commit()
            cn.close()
        except Exception as e:
            print(e)
        # print("hello",updated_data)
        # updated_data=[{
        #
        #         'sr_no':item_id['sr_no'],
        #         'Purchase_Order_no':'23234243'
        #         # Add other fields as needed
        #     }]
    print(updated_data)
    return updated_data



@app.route('/upload-endpoint', methods=['POST'])
def upload_endpoint():
    try:
        # print('updatefunction')
        selected_rows = request.form.get('selectedRows')#['selectedRows']

        # print('update',selected_rows)

        # Process the selected rows, update posting details, etc.
        # Return the updated data as response
        updated_data = process_selected_rows(selected_rows)
        return jsonify(updated_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/form')
def form():
    return render_template('form.html')



# For Python Bootstrap
if __name__ == "__main__":
    app.run()
