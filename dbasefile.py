from pymysql import *
import pandas as pd
import os
import pymysql.cursors
from datetime import *
def dbfun():
    global cn
    cn = connect(host="centralinward.ckvbu2zjskqc.ap-south-1.rds.amazonaws.com",user="admin",password="Well#&ne$$^",db='testdb')
    c = cn.cursor(pymysql.cursors.DictCursor)
    return cn,c

def sybasedb():
    host = "UAT_04m00021_cl"
    database = "04M00021"
    username = "data"
    password = "D@1@<>3"
    global conn
    cs = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (host, username, password, database)
    conn = pyodbc.connect(cs)
    cur = conn.cursor()
    return conn,cur


def item_master(code):
    cn,cur=dbfun()
    if len(code)==1:
        cur.execute(f"SELECT c_code,c_name FROM testdb2.item_mst where c_code = '{code[0]}' ")
    else:
        cur.execute(f"SELECT c_code,c_name FROM testdb2.item_mst where c_code in {code} ")
    itm=cur.fetchall()
    return itm

def supp_master(code):
    cn, cur = dbfun()
    if len(code) == 1:
        cur.execute(f"SELECT c_code,c_name FROM testdb2.act_mst where n_type='5' and c_code = '{code[0]}' ")
    else:
        cur.execute(f"SELECT c_code,c_name FROM testdb2.act_mst where n_type='5' and c_code in {code}")
    supp = cur.fetchall()
    return supp

def br_master(code):
    cn, cur = dbfun()
    print(code)
    if len(code) == 1:
        cur.execute(f"SELECT c_code,c_name FROM testdb2.act_mst where n_type='3' and c_code = '{code[0]}' ")
    else:
        cur.execute(f"SELECT c_code,c_name FROM testdb2.act_mst where n_type='3' and c_code in {code}")
    br = cur.fetchall()
    print(br)
    return br


def file_with_supp_item(file):
    df=pd.read_csv(rf'{file}')
    supp_code=tuple(df['supplier_code'].unique())
    item_code = tuple(df['item_code'].unique())
    br_code = tuple(df['br_code'].unique())
    itm_code=item_master(item_code)
    sup_code = supp_master(supp_code)
    br_code = br_master(br_code)
    print('List',itm_code,'filee',sup_code,'br_code',br_code)
    data_item={}
    for i in itm_code:
        print(i['c_code'],i['c_name'])
        data_item[i['c_code']]=i['c_name']
    print(data_item,'item')
    data_sup={}
    for i in sup_code:
        print(i['c_code'], i['c_name'])
        data_sup[i['c_code']]=i['c_name']

    data_br = {}
    for i in br_code:
        print(i['c_code'], i['c_name'])
        data_br[i['c_code']] = i['c_name']

    print(data_sup, 'supp')
    print(data_br,'br')
    df['item_code']=df['item_code'].astype('str')
    df['br_code'] = df['br_code'].astype('str')
    df['Supplier_name']=df['supplier_code'].map(data_sup)
    df['Item_name'] = df['item_code'].map(data_item)
    df['Branch_name'] = df['br_code'].map(data_br)
    df.to_csv(os.path.join('samples', 'data.csv'))

    return df



def convert_supp_item_count(file):
    df=pd.read_csv(rf'{file}')

    f=df.groupby('supplier_code')['item_code'].count()
    print(f)
    for i in f:
        print(i)




    # supp_code=tuple(df['supplier_code'].unique())
    # item_code = tuple(df['item_code'].unique())
    # br_code = tuple(df['br_code'].unique())
    # itm_code=item_master(item_code)
    # sup_code = supp_master(supp_code)
    # br_code = br_master(br_code)
    # print('List',itm_code,'filee',sup_code,'br_code',br_code)
    # data_item={}
    # for i in itm_code:
    #     print(i['c_code'],i['c_name'])
    #     data_item[i['c_code']]=i['c_name']
    # print(data_item,'item')
    # data_sup={}
    # for i in sup_code:
    #     print(i['c_code'], i['c_name'])
    #     data_sup[i['c_code']]=i['c_name']
    #
    # data_br = {}
    # for i in br_code:
    #     print(i['c_code'], i['c_name'])
    #     data_br[i['c_code']] = i['c_name']
    #
    # print(data_sup, 'supp')
    # print(data_br,'br')
    # df['item_code']=df['item_code'].astype('str')
    # df['br_code'] = df['br_code'].astype('str')
    # df['Supplier_name']=df['supplier_code'].map(data_sup)
    # df['Item_name'] = df['item_code'].map(data_item)
    # df['Branch_name'] = df['br_code'].map(data_br)
    # df.to_csv(os.path.join('samples', 'data.csv'))

    return f














