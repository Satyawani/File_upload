from pymysql import *
import pandas as pd
import numpy as np
import os
import pymysql.cursors
import re
from datetime import *
ip='192.168.250.50'
portno='43503'

# ip='192.168.250.101'
# portno='23503'


# http://192.168.250.50:43503/ws_pot_po?json=
# http://192.168.250.50:43503/ws_pot_po?json=

post_url=f'http//{ip}:{portno}/ws_pot_po?json='

post_url='http://192.168.249.172:43503/ws_pot_po?json='

def clean_text(text):
    # Remove special characters and spaces from text
    return re.sub(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\]', '', text)

def dbfun():
    global cn
    cn = connect(host="centralinward.ckvbu2zjskqc.ap-south-1.rds.amazonaws.com",user="admin",password="Well#&ne$$^",db='testdb')
    c = cn.cursor(pymysql.cursors.DictCursor)
    return cn,c




def item_master(code):
    cn,cur=dbfun()
    if len(code)==1:
        cur.execute(f"SELECT c_code,c_name,n_qty_per_box FROM testdb.item_mst where c_code = '{code[0]}' ")
    else:
        cur.execute(f"SELECT c_code,c_name,n_qty_per_box FROM testdb.item_mst where c_code in {code} ")
    itm=cur.fetchall()
    return itm

def supp_master(code):
    cn, cur = dbfun()
    if len(code) == 1:
        cur.execute(f"SELECT c_code,c_name FROM testdb.act_mst where n_type='5' and c_code = '{code[0]}' ")
    else:
        cur.execute(f"SELECT c_code,c_name FROM testdb.act_mst where n_type='5' and c_code in {code}")
    supp = cur.fetchall()
    return supp

def br_master(code):
    cn, cur = dbfun()
    print(code)
    if len(code) == 1:
        cur.execute(f"SELECT c_code,c_name FROM testdb.act_mst where n_type='3' and c_code = '{code[0]}' ")
    else:
        cur.execute(f"SELECT c_code,c_name FROM testdb.act_mst where n_type='3' and c_code in {code}")
    br = cur.fetchall()
    # print(br)
    return br


def item_wise_eff_pur(code):
    cn, cur = dbfun()
    print(code,f"SELECT c_item_code,n_eff_pur_rate FROM testdb.item_wise_last_eff_pur_rate where c_item_code in {code}")
    if len(code) == 1:
        cur.execute(f"SELECT c_item_code,n_eff_pur_rate FROM testdb.item_wise_last_eff_pur_rate where  c_item_code = '{code[0]}' ")
    else:
        cur.execute(f"SELECT c_item_code,n_eff_pur_rate FROM testdb.item_wise_last_eff_pur_rate where c_item_code in {code}")
    br = cur.fetchall()
    print('rate',br)
    return br



def file_with_supp_item(file):
    try:
        df=pd.read_csv(rf'samples/{file}',skipinitialspace = True,converters={"item_code":str,"br_code":str})
        # print(df.dtypes)
        # df['item_code']=df['item_code'].astype('str')
        # df['br_code'] = df['br_code'].astype('str')
        # df['supplier_code'] = df['supplier_code'].apply(clean_text)
        # print(df['br_code'])
        # df['item_code'] = df['item_code'].apply(clean_text)
        # print(df['item_code'])
        # df['br_code'] = df['br_code'].apply(clean_text)
        # print(df['item_code'])
        duplicate_item_codes = df.groupby('supplier_code')['item_code'].filter(lambda x: x.duplicated().any())
        (df['item_code'])
        if not duplicate_item_codes.empty:
            print(df['item_code'])
            raise ValueError("Duplicate item codes found within the same supplier group")

        supp_code=tuple(df['supplier_code'].unique())
        item_code = tuple(df['item_code'].unique())
        br_code = tuple(df['br_code'].unique())
        itm_code=item_master(item_code)
        sup_code = supp_master(supp_code)
        br_code = br_master(br_code)
        # print('brcode_1',br_code)
        rate = item_wise_eff_pur(item_code)
        # print('List',itm_code,'filee',sup_code,'br_code',br_code,rate)
        data_item={}
        for i in itm_code:
            # print(i['c_code'],i['c_name'])
            data_item[i['c_code']]=i['c_name']

        # print(data_item,'item')
        data_sup={}
        for i in sup_code:
            # print(i['c_code'], i['c_name'])
            data_sup[i['c_code']]=i['c_name']

        data_br = {}
        for i in br_code:
            # print(i['c_code'], i['c_name'])
            data_br[i['c_code']] = i['c_name']

        data_rate = {}
        for i in rate:
            # print(i['c_item_code'], i['n_eff_pur_rate'])
            data_rate[i['c_item_code']] = i['n_eff_pur_rate']
        # print(data_rate, 'item')

        data_qty_per_box = {}
        for i in itm_code:
            print(i['c_code'], i['n_qty_per_box'])
            data_qty_per_box[i['c_code']] = i['n_qty_per_box']
        # print(data_qty_per_box, 'item')

        # print(data_sup, 'supp')
        # print(data_br,'br')
        df['item_code']=df['item_code'].astype('str')
        df['br_code'] = df['br_code'].astype('str')
        df['Supplier_name']=df['supplier_code'].map(data_sup)
        df['Item_name'] = df['item_code'].map(data_item)
        df['Branch_name'] = df['br_code'].map(data_br)
        df['rate'] = df['item_code'].map(data_rate)
        df['qty_per_box'] = df['item_code'].map(data_qty_per_box)
        df['qty_calc'] =df['qty_per_box']*df['qty']
        df['rate'][df['rate'].isna()==True]=0
        # print(df['rate'])
        df['line_level_rate']=df['rate']*df['qty_per_box']
        df['total']=df['line_level_rate']*df['qty']
        # print(df['rate'])
        df=df[['br_code','Branch_name','supplier_code','Supplier_name','item_code','Item_name','qty','line_level_rate','qty_calc','total']]
        df.to_csv("samples/data.csv")
        # df.to_csv('data.csv',index=False)

        return df
    except Exception as e:
        print(e)

        df=pd.DataFrame()
        df.to_csv("samples/data.csv")

        return df

# Function to split lists with length > 2
def split_lists(row):
    if len(row) > 4:
        num_splits = len(row) // 2
        extra_elements = len(row) % 2
        new_rows = [row[i * 2:(i + 1) * 2] for i in range(num_splits)]
        if extra_elements > 0:
            new_rows.append(row[-extra_elements:])
        return new_rows
    else:
        return [row]

def convert_supp_item_count(file):
    # df=pd.read_csv(rf'samples/aggr_data.csv')

    # file = pd.read_csv(r'data.csv')

    df = file.groupby(['br_code', 'supplier_code']).agg(
    item_Details=('item_code', lambda x: x.tolist()),
    qty_value=('qty_calc', lambda x: x.tolist()),
        supplier_name=('Supplier_name', 'first'),
    item_Count=('item_code', 'size'),
        qty=('qty', lambda x: x.tolist()),
        rate_Details=('line_level_rate', lambda x: x.tolist()),

    rate_sum=('line_level_rate', 'sum'),
    total_sum=('total', lambda x: x.tolist())
    ).reset_index()
    df.to_csv("Testing_file_total.csv",index=False)

    #total_sum=('total', 'sum')


    # print(df)
    # print(df['item_Details'])
    # Create a new DataFrame to hold the split rows
    # Create a new DataFrame to hold the split rows
    split_df = pd.DataFrame(columns=df.columns)

    # Iterate over each row in the original DataFrame
    # for index, row in df.iterrows():
    #     item_code = row['item_Details']
    #     qty = row['qty_value']
    #     item_code_len = len(item_code)
    #     if item_code_len > 50:
    #         num_splits = item_code_len // 50
    #         extra_elements = item_code_len % 50
    #         for i in range(num_splits):
    #             new_row = row.copy()
    #             new_row['item_Details'] = item_code[i*2:(i+1)*2]
    #             new_row['qty_value'] = qty[i*2:(i+1)*2]
    #             new_row['item_Count'] = len(new_row['item_Details'])
    #
    #             split_df = split_df._append(new_row, ignore_index=True)
    #         if extra_elements > 0:
    #             new_row = row.copy()
    #             new_row['item_Details'] = item_code[-extra_elements:]
    #             new_row['qty_value'] = qty[-extra_elements:]
    #             new_row['item_Count'] = len(new_row['item_Details'])
    #             split_df = split_df._append(new_row, ignore_index=True)
    #     else:
    #         row['item_Count'] = item_code_len
    #         split_df = split_df._append(row, ignore_index=True)

    # ...
    for index, row in df.iterrows():
        item_code = row['item_Details']
        qty = row['qty_value']
        total = row['total_sum']
        rate = row['rate_Details']
        qty_valu = row['qty_value']



        item_code_len = len(item_code)
        max_elements_per_row = 25  # Change this to the desired maximum number of elements per row

        if item_code_len > max_elements_per_row:
            num_splits = item_code_len // max_elements_per_row
            extra_elements = item_code_len % max_elements_per_row

            for i in range(num_splits):
                new_row = row.copy()
                start_idx = i * max_elements_per_row
                end_idx = (i + 1) * max_elements_per_row
                new_row['item_Details'] = item_code[start_idx:end_idx]
                new_row['qty_value'] = qty[start_idx:end_idx]
                new_row['total_sum'] = sum(total[start_idx:end_idx])
                new_row['rate_Details'] = rate[start_idx:end_idx]
                new_row['qty_value'] = qty_valu[start_idx:end_idx]

                new_row['item_Count'] = len(new_row['item_Details'])
                print('total',sum(total[start_idx:end_idx]))



                split_df = split_df._append(new_row, ignore_index=True)

            if extra_elements > 0:
                new_row = row.copy()
                new_row['item_Details'] = item_code[-extra_elements:]
                new_row['qty_value'] = qty[-extra_elements:]
                new_row['item_Count'] = len(new_row['item_Details'])
                new_row['total_sum'] = sum(total[-extra_elements:])
                new_row['rate_Details'] = rate[-extra_elements:]
                new_row['qty_value'] = qty_valu[-extra_elements:]
                print('total', sum(total[-extra_elements:]))
                split_df = split_df._append(new_row, ignore_index=True)
        else:
            row['item_Count'] = item_code_len
            row['total_sum'] = sum(total)
            row['rate_Details'] = rate
            row['qty_value'] = qty_valu
            split_df = split_df._append(row, ignore_index=True)
    # ...

    split_df['total_sum'] = split_df['total_sum'].round(2)
    split_df['sr_no'] = range(1, len(split_df) + 1)
    split_df['Purchase_Order_no'] =''
    # print(split_df)# # Apply the function to the column
    # df['item_Details'] = df['item_Details'].apply(split_lists)
    #
    # df = df.explode('item_Details').reset_index(drop=True)
    #
    # print(df['item_Details'])
    split_df.to_csv('aggr_data.csv',index=False)

    return split_df












