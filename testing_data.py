import json
from app_config_file import *


def supplier_action(data):
    print(data)
    # if data['model'] =="supplier":
    #     if data['event'] =="entry.publish":
    #         print('publish')
    #         data_1=create_supplier_mapped_to_netsuite(data['entry'])
    #         return data_1
    #     elif data['event'] =="entry.update":
    #         data_1=update_supplier_mapped_to_netsuite(data['entry'])
    #         return data_1
    #     elif data['event'] =="entry.delete":
    #         data_1=delete_supplier_mapped_to_netsuite(data['entry'])
    #         return data_1

    # else:
    #     return "No record Found"

    if data['model'] == "supplier":
        if data['netsuite_id'] == None:
            print('create')
            data_1 = create_supplier_mapped_to_netsuite(data['entry'])
            return data_1
        else:
            print('update')
            data_1 = update_supplier_mapped_to_netsuite(data['entry'])
            return data_1
    else:
        return "No record Found"


def create_supplier_mapped_to_netsuite(data):
    try:
        # data=create_supplier(data)
        if data != "No record Found":
            print("example:!2", data)
            # or (data['isindividual']==None)

            # if (data['isindividual']==False) :
            #     data['isindividual']="NO"
            # elif (data['isindividual']==True):
            #     data['isindividual']="YES"
            # else:
            #     data['isindividual']=None

            if ((len(data['pan_number'])) >= 4) and (data['pan_number'][3] == "P"):
                data['isindividual'] = "YES"
                first_name, last_name = data['supplier_name'].split()
            else:
                data['isindividual'] = "NO"

            # or (data['is_billingaddrss_same']==None)
            if (data['is_billingaddrss_same'] == False):
                data['is_billingaddrss_same'] = "NO"
            elif (data['is_billingaddrss_same'] == True):
                data['is_billingaddrss_same'] = "YES"
            else:
                data['is_billingaddrss_same'] = None

            if len(data['Shipping_address']) == 1:
                addr_supp = data['Shipping_address'][0]
                addr_supp_1 = {"vendor_address1": addr_supp['address_1'], "vendor_address2": addr_supp['address_2'],
                               "vendor_attention": "", "vendor_city": addr_supp['city'],
                               "vendor_state": addr_supp['state'], "vendor_country": addr_supp['country_code'],
                               "vendor_zip": addr_supp['pincode']}

            if len(data['Billing_address']) == 1:
                addr_supp = data['Billing_address'][0]
                addr_supp_2 = {"vendor_address1": addr_supp['address_1'], "vendor_address2": addr_supp['address_2'],
                               "vendor_attention": "", "vendor_city": addr_supp['city'],
                               "vendor_state": addr_supp['state'], "vendor_country": addr_supp['country_code'],
                               "vendor_zip": addr_supp['pincode']}

            if data['subsidiary'] == 'Wellness Forever parent Company':
                data['subsidiary'] = '1'
            elif data['subsidiary'] == 'Wellness Forever Elimination Subsidiary':
                data['subsidiary'] = '8'
            elif data['subsidiary'] == 'Wellness Forever Medicare Limited':
                data['subsidiary'] = '4'
            elif data['subsidiary'] == 'Amore Health Essentials Private Limited':
                data['subsidiary'] = '5'
            elif data['subsidiary'] == 'Wellness Forever Healthtech Private Limited':
                data['subsidiary'] = '6'
            else:
                data['subsidiary'] = None

            if data['supplier_type'] == 'Consultant':
                data['supplier_type'] = '2'
            elif data['supplier_type'] == 'Digital Asset Vendors':
                data['supplier_type'] = '6'
            elif data['supplier_type'] == 'Direct - Contract Manufacturing':
                data['supplier_type'] = '10'
            elif data['supplier_type'] == 'Direct - Packaging':
                data['supplier_type'] = '9'
            elif data['supplier_type'] == 'Distributor':
                data['supplier_type'] = '12'
            elif data['supplier_type'] == 'Digital Asset Vendors':
                data['supplier_type'] = '6'
            elif data['supplier_type'] == 'Direct - Contract Manufacturing':
                data['supplier_type'] = '10'
            elif data['supplier_type'] == 'Direct - Packaging':
                data['supplier_type'] = '9'
            elif data['supplier_type'] == 'Distributor':
                data['supplier_type'] = '12'
            elif data['supplier_type'] == 'Franchise':
                data['supplier_type'] = '5'
            elif data['supplier_type'] == 'Manufacture':
                data['supplier_type'] = '11'
            elif data['supplier_type'] == 'Other':
                data['supplier_type'] = '13'
            elif data['supplier_type'] == 'Standard ':
                data['supplier_type'] = '7'
            elif data['supplier_type'] == 'Supplies':
                data['supplier_type'] = '4'
            elif data['supplier_type'] == 'Tax agency':
                data['supplier_type'] = '3'
            elif data['supplier_type'] == 'Turnkey Vendor':
                data['supplier_type'] = '8'


            else:
                data['supplier_type'] = None

            # str(data['supplier_type']),

            netsuite = {
                'subsidiary': data['subsidiary'],
                'vendor_id': data['supplier_code'],
                'isindividual': data['isindividual'],
                'type': 'create',
                'vendor_email': data['business_email_id'],
                'vendor_phone': data['business_mobile_number'],
                'vendor_creditlimit': data['supplier_credit_limit_per_month'],
                'vendor_taxnumber': data['tan_number'],
                'vendor_terms': data['vendor_terms'],
                'vendor_category': '',
                'vendor_type': data['supplier_type'],
                'print_name': data['print_name'],
                'supplier_credit_days': data['supplier_credit_days'],
                'supplier_due_date': data['supplier_due_date_on'],
                'isactive': '',
                'micr_number': data['micr_number'],
                'due_date_method': data['due_date_method'],
                'expiry_method': data['expiry_method'],
                'pan_number': data['pan_number'],
                'payableby_branch': data['payable_by_branch_only'],
                'bank_code': '',
                'bank_name': data['bank_name'],
                'account_holder_name': data['account_holder_name'],
                'account_number': data['account_no'],
                'ifsc_code': data['ifsc_code'],
                'tax_registration_details': {
                    'country': '',
                    'nexus': '',
                    'nexus_state': '',
                    'tax_registration_number': data['gstn_no']
                },
                'is_billingaddrss_same': data['is_billingaddrss_same']
            }

            print(netsuite)

            if netsuite['is_billingaddrss_same'] == 'YES':
                netsuite['vendor_billing_address'] = addr_supp_1
                netsuite['vendor_shipping_address'] = addr_supp_1
            elif netsuite['is_billingaddrss_same'] == 'NO':
                netsuite['vendor_billing_address'] = addr_supp_2
                netsuite['vendor_shipping_address'] = addr_supp_1
            else:
                netsuite['vendor_billing_address'] = None
                netsuite['vendor_shipping_address'] = None

            if first_name:
                netsuite['vendor_first_name'] = first_name
            elif last_name:
                netsuite['vendor_last_name'] = last_name
            else:
                netsuite['company_name'] = data['supplier_name']

            print(type(netsuite), 'data', json.dumps(netsuite))
            # json_object = json.loads(netsuite)

            # print(type(json_object))
            print()
            response = oauth.post(URL, data=json.dumps(netsuite), headers=headers)
            print(response, response.text)
            print('Result', response.json())
            data_rep = response.json()
            print(data_rep)
            if data_rep['status'] == 200:
                api_mdm = mdm_api + '/' + str(data['id'])
                print(api_mdm)

                data_1 = {"data": {"netsuite_id": str(data_rep['vendorId'])}}
                # print(json.dumps(data_1))

                response = requests.request("PUT", api_mdm, headers=headers, data=json.dumps(data_1))
                print(response.text)

            return {
                'statusCode': 200,
                'body': json.dumps(response.text)
            }
        else:
            return {
                'statusCode': 400,
                'body': str("No Record Found")
            }
    except Exception as e:
        print(f"exception while processing message: {repr(e)}")
        return {
            'statusCode': 500,
            'body': repr(e)
        }


def update_supplier_mapped_to_netsuite(data):
    try:
        # data=create_supplier(data)
        if data != "No record Found":
            print("example:!2", data)

            # if (data['isindividual']==False) or (data['isindividual']==None) :
            #     data['isindividual']="NO"
            # else:
            #     data['isindividual']="YES"

            if (len(data['pan_number']) >= 4 and data['pan_number'][3] == "P"):
                data['isindividual'] = "YES"
            else:
                data['isindividual'] = "NO"

            if (data['is_billingaddrss_same'] == False) or (data['is_billingaddrss_same'] == None):
                data['is_billingaddrss_same'] = "NO"
            else:
                data['is_billingaddrss_same'] = "YES"

            if len(data['Shipping_address']) == 1:
                addr_supp = data['Shipping_address'][0]
                addr_supp_1 = {"vendor_address1": addr_supp['address_1'], "vendor_address2": addr_supp['address_2'],
                               "vendor_attention": "", "vendor_city": addr_supp['city'],
                               "vendor_state": addr_supp['state'], "vendor_country": addr_supp['country_code'],
                               "vendor_zip": addr_supp['pincode']}

            if len(data['Billing_address']) == 1:
                addr_supp = data['Billing_address'][0]
                addr_supp_2 = {"vendor_address1": addr_supp['address_1'], "vendor_address2": addr_supp['address_2'],
                               "vendor_attention": "", "vendor_city": addr_supp['city'],
                               "vendor_state": addr_supp['state'], "vendor_country": addr_supp['country_code'],
                               "vendor_zip": addr_supp['pincode']}

            netsuite = {
                'subsidiary': data['subsidiary'],
                'vendor_id': data['supplier_code'],
                'isindividual': data['isindividual'],
                'type': 'update',
                'vendor_email': data['business_email_id'],
                'vendor_phone': data['business_mobile_number'],
                'vendor_creditlimit': data['supplier_credit_limit_per_month'],
                'vendor_taxnumber': data['tan_number'],
                'vendor_category': '',
                'vendor_type': data['supplier_type'],
                'print_name': data['print_name'],
                'supplier_credit_days': data['supplier_credit_days'],
                'supplier_due_date': data['supplier_due_date_on'],
                'isactive': '',
                'micr_number': data['micr_number'],
                'due_date_method': data['due_date_method'],
                'expiry_method': data['expiry_method'],
                'pan_number': data['pan_number'],
                'payableby_branch': data['payable_by_branch_only'],
                'bank_code': '',
                'bank_name': data['bank_name'],
                'account_holder_name': data['account_holder_name'],
                'account_number': data['account_no'],
                'ifsc_code': data['ifsc_code'],
                'tax_registration_details': {
                    'country': '',
                    'nexus': '',
                    'nexus_state': '',
                    'tax_registration_number': data['gstn_no'],
                },
                'vendor_terms': data['vendor_terms'],
                'is_billingaddrss_same': data['is_billingaddrss_same']
            }

            print(netsuite)

            if netsuite['is_billingaddrss_same'] == 'Yes':
                netsuite['vendor_billing_address'] = addr_supp_1
                netsuite['vendor_shipping_address'] = addr_supp_1
            else:
                netsuite['vendor_billing_address'] = addr_supp_2
                netsuite['vendor_shipping_address'] = addr_supp_1

            if first_name:
                netsuite['vendor_first_name'] = first_name
            elif last_name:
                netsuite['vendor_last_name'] = last_name
            else:
                netsuite['company_name'] = data['supplier_name']

            print(type(netsuite), 'data', netsuite)
            # json_object = json.loads(netsuite)

            # print(type(json_object))
            print()
            response = oauth.post(URL, data=netsuite, headers=headers)
            print(response, response.text)
            print('Result', response.json())

            return {
                'statusCode': 200,
                'body': json.dumps(response.json())
            }
        else:
            return {
                'statusCode': 400,
                'body': str("No Record Found")
            }

    except Exception as e:
        print(f"exception while processing message: {repr(e)}")
        return {
            'statusCode': 500,
            'body': repr(e)
        }


def delete_supplier_mapped_to_netsuite(data):
    try:
        # data=create_supplier(data)
        if data != "No record Found":
            print("example:!2", data)

            # if (data['isindividual']==False) or (data['isindividual']==None) :
            #     data['isindividual']="NO"
            # else:
            #     data['isindividual']="YES"

            if (len(data['pan_number']) >= 4 and data['pan_number'][3] === "P"):
                data['isindividual'] = "YES"
            else:
                data['isindividual'] = "NO"

            if (data['is_billingaddrss_same'] == False) or (data['is_billingaddrss_same'] == None):
                data['is_billingaddrss_same'] = "NO"
            else:
                data['is_billingaddrss_same'] = "YES"

            if len(data['Shipping_address']) == 1:
                addr_supp = data['Shipping_address'][0]
                addr_supp_1 = {"vendor_address1": addr_supp['address_1'], "vendor_address2": addr_supp['address_2'],
                               "vendor_attention": "", "vendor_city": addr_supp['city'],
                               "vendor_state": addr_supp['state'], "vendor_country": addr_supp['country_code'],
                               "vendor_zip": addr_supp['pincode']}

            if len(data['Billing_address']) == 1:
                addr_supp = data['Billing_address'][0]
                addr_supp_2 = {"vendor_address1": addr_supp['address_1'], "vendor_address2": addr_supp['address_2'],
                               "vendor_attention": "", "vendor_city": addr_supp['city'],
                               "vendor_state": addr_supp['state'], "vendor_country": addr_supp['country_code'],
                               "vendor_zip": addr_supp['pincode']}

            netsuite = {'company_name': 'Wellnessforever', 'type': 'delete', 'vendor_email': data['business_email_id']}

            print(netsuite)

            if netsuite['is_billingaddrss_same'] == 'Yes':
                netsuite['vendor_billing_address'] = addr_supp_1
                netsuite['vendor_shipping_address'] = addr_supp_1
            else:
                netsuite['vendor_billing_address'] = addr_supp_2
                netsuite['vendor_shipping_address'] = addr_supp_1

            print(type(netsuite), 'data', netsuite)
            # json_object = json.loads(netsuite)

            # print(type(json_object))
            print()
            response = oauth.post(URL, data=netsuite, headers=headers)
            print(response, response.text)
            print('Result', response.json())

            return {
                'statusCode': 200,
                'body': json.dumps(response.json())
            }
        else:
            return {
                'statusCode': 400,
                'body': str("No Record Found")
            }
    except Exception as e:
        print(f"exception while processing message: {repr(e)}")
        return {
            'statusCode': 500,
            'body': repr(e)
        }


def lambda_handler(event, context):
    try:
        data = supplier_action(event)

        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': repr(e)
        }

