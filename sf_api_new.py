#To run program:  python3 fth_api.py prashant

#README:  if conn error make sure password is set properly in RDS PASSWORD section

#README:  Debug Mode may need to be set to Fales when deploying live (although it seems to be working through Zappa)

#README:  if there are errors, make sure you have all requirements are loaded
#pip3 install flask
#pip3 install flask_restful
#pip3 install flask_cors
#pip3 install Werkzeug
#pip3 install pymysql
#pip3 install python-dateutil
#pip3 install boto3
#pip3 install stripe
#pip3 install bs4

import os
import uuid
import boto3
import json
import math
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import random
import string
import stripe

from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_mail import Mail, Message
# used for serializer email and error handling
#from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
#from flask_cors import CORS

from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import generate_password_hash, \
     check_password_hash


#  NEED TO SOLVE THIS
# from NotificationHub import Notification
# from NotificationHub import NotificationHub
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

from dateutil.relativedelta import *
from decimal import Decimal
from datetime import datetime, date, timedelta
from hashlib import sha512
from math import ceil
import string
import random
# BING API KEY
# Import Bing API key into bing_api_key.py

#  NEED TO SOLVE THIS
# from env_keys import BING_API_KEY, RDS_PW

import decimal
import sys
import json
import pytz
import pymysql
import requests

#RDS_HOST = 'pm-mysqldb.cxjnrciilyjq.us-west-1.rds.amazonaws.com'
RDS_HOST = 'io-mysqldb8.cxjnrciilyjq.us-west-1.rds.amazonaws.com'
#RDS_HOST = 'localhost'
RDS_PORT = 3306
#RDS_USER = 'root'
RDS_USER = 'admin'
#RDS_DB = 'feed_the_hungry'
RDS_DB = 'sf'

#app = Flask(__name__)
app = Flask(__name__, template_folder='assets')

# --------------- Stripe Variables ------------------
# these key are using for testing. Customer should use their stripe account's keys instead
import stripe
stripe_public_key = 'pk_test_6RSoSd9tJgB2fN2hGkEDHCXp00MQdrK3Tw'
stripe_secret_key = 'sk_test_fe99fW2owhFEGTACgW3qaykd006gHUwj1j'

#this is a testing key using ptydtesting's stripe account.
# stripe_public_key = "pk_test_51H0sExEDOlfePYdd9TVlnhVDOCmmnmdxAxyAmgW4x7OI0CR7tTrGE2AyrTk8VjftoigEOhv2RTUv5F8yJrfp4jWQ00Q6KGXDHV"
# stripe_secret_key = "sk_test_51H0sExEDOlfePYdd9UQDxfp8yoY7On272hCR9ti12WSNbIGTysaJI8K2W8NhCKqdBOEhiNj4vFOtQu6goliov8vF00cvqfWG6d"

stripe.api_key = stripe_secret_key
# Allow cross-origin resource sharing
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ''

# Setting for mydomain.com
app.config['MAIL_SERVER'] = 'smtp.mydomain.com'
app.config['MAIL_PORT'] = 465

# Setting for gmail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465

app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Set this to false when deploying to live application
#app.config['DEBUG'] = True
app.config['DEBUG'] = False

app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')

mail = Mail(app)

# API
api = Api(app)

# convert to UTC time zone when testing in local time zone
utc = pytz.utc
def getToday(): return datetime.strftime(datetime.now(utc), "%Y-%m-%d")
def getNow(): return datetime.strftime(datetime.now(utc),"%Y-%m-%d %H:%M:%S")

# Get RDS password from command line argument
def RdsPw():
    if len(sys.argv) == 2:
        return str(sys.argv[1])
    return ""

# RDS PASSWORD
# When deploying to Zappa, set RDS_PW equal to the password as a string
# When pushing to GitHub, set RDS_PW equal to RdsPw()
RDS_PW = 'prashant'
# RDS_PW = RdsPw()


s3 = boto3.client('s3')

# aws s3 bucket where the image is stored
# BUCKET_NAME = os.environ.get('MEAL_IMAGES_BUCKET')
BUCKET_NAME = 'servingnow'
# allowed extensions for uploading a profile photo file
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



getToday = lambda: datetime.strftime(date.today(), "%Y-%m-%d")
getNow = lambda: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

# For Push notification
isDebug = False
NOTIFICATION_HUB_KEY = os.environ.get('NOTIFICATION_HUB_KEY')
NOTIFICATION_HUB_NAME = os.environ.get('NOTIFICATION_HUB_NAME')

# Connect to MySQL database (API v2)
def connect():
    global RDS_PW
    global RDS_HOST
    global RDS_PORT
    global RDS_USER
    global RDS_DB

    print("Trying to connect to RDS (API v2)...")
    try:
        conn = pymysql.connect( RDS_HOST,
                                user=RDS_USER,
                                port=RDS_PORT,
                                passwd=RDS_PW,
                                db=RDS_DB,
                                cursorclass=pymysql.cursors.DictCursor)
        print("Successfully connected to RDS. (API v2)")
        return conn
    except:
        print("Could not connect to RDS. (API v2)")
        raise Exception("RDS Connection failed. (API v2)")

# Disconnect from MySQL database (API v2)
def disconnect(conn):
    try:
        conn.close()
        print("Successfully disconnected from MySQL database. (API v2)")
    except:
        print("Could not properly disconnect from MySQL database. (API v2)")
        raise Exception("Failure disconnecting from MySQL database. (API v2)")

# Serialize JSON
def serializeResponse(response):
    try:
        print("In Serialize JSON")
        for row in response:
            for key in row:
                if type(row[key]) is Decimal:
                    row[key] = float(row[key])
                elif type(row[key]) is date or type(row[key]) is datetime:
                    row[key] = row[key].strftime("%Y-%m-%d")
        print("In Serialize JSON response", response)
        return response
    except:
        raise Exception("Bad query JSON")








# Execute an SQL command (API v2)
# Set cmd parameter to 'get' or 'post'
# Set conn parameter to connection object
# OPTIONAL: Set skipSerialization to True to skip default JSON response serialization
def execute(sql, cmd, conn, skipSerialization = False):
    response = {}
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if cmd is 'get':
                result = cur.fetchall()
                response['message'] = 'Successfully executed SQL query.'
                # Return status code of 280 for successful GET request
                response['code'] = 280
                if not skipSerialization:
                    result = serializeResponse(result)
                response['result'] = result
            elif cmd in 'post':
                conn.commit()
                response['message'] = 'Successfully committed SQL command.'
                # Return status code of 281 for successful POST request
                response['code'] = 281
            else:
                response['message'] = 'Request failed. Unknown or ambiguous instruction given for MySQL command.'
                # Return status code of 480 for unknown HTTP method
                response['code'] = 480
    except:
        response['message'] = 'Request failed, could not execute MySQL command.'
        # Return status code of 490 for unsuccessful HTTP request
        response['code'] = 490
    finally:
        response['sql'] = sql
        return response


# Close RDS connection
def closeRdsConn(cur, conn):
    try:
        cur.close()
        conn.close()
        print("Successfully closed RDS connection.")
    except:
        print("Could not close RDS connection.")

# Runs a select query with the SQL query string and pymysql cursor as arguments
# Returns a list of Python tuples
def runSelectQuery(query, cur):
    try:
        cur.execute(query)
        queriedData = cur.fetchall()
        return queriedData
    except:
        raise Exception("Could not run select query and/or return data")




















# -- Queries start here -------------------------------------------------------------------------------


# QUERY 1  BUSINESSES
class Businesses(Resource):
    # QUERY 1 RETURNS ALL BUSINESSES
    def get(self):
        response = {}
        items = {}
        try:
            conn = connect()
            query = """ # QUERY 1 RETURNS ALL BUSINESSES
                SELECT * FROM sf.businesses; """
            items = execute(query, 'get', conn)

            response['message'] = 'Businesses successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


    # # QUERY 1A UPDATES A SPECIFIC FIELD IN A SPECIFIC BUSINESSES
    # def post(self):
    #     response = {}
    #     items = {}
    #     try:
    #         conn = connect()
    #         data = request.get_json(force=True)
    #         BusinessId = data['business_id']
    #         updatedBusinessName = data['business_name']
    #         query =  '''
    #                 UPDATE  sf.businesses
    #                 SET business_name = \'''' + updatedBusinessName + '''\'
    #                 WHERE business_id = \'''' + BusinessId + '''\';
    #                 '''
    #         items = execute(query,'post',conn)

    #         response['message'] = 'Businesses Post successful'
    #         response['result'] = items
    #         return response, 200
    #     except:
    #         raise BadRequest('Q1A Request failed, please try again later.')
    #     finally:
    #         disconnect(conn)

    #     # ENDPOINT AND JSON OBJECT THAT WORKS
    #     # http://localhost:4000/api/v2/businesses
    #     # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/businesses
    #     # {"business_id":"200-000001",
    #     #  "business_name":"Infinite Options"}


    # QUERY 1B UPDATES A SPECIFIC JSON FIELD IN A SPECIFIC BUSINESSES
    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()
            data = request.get_json(force=True)
            BusinessId = data['business_id']
            updatedAcceptingHours = data['business_accepting_hours']
            print("updatedAcceptingHours= ",  updatedAcceptingHours)
            query =  '''
                    UPDATE  sf.businesses
                    SET business_accepting_hours = \'''' + updatedAcceptingHours + '''\'
                    WHERE business_uid = \'''' + BusinessId + '''\';
                    '''
            items = execute(query,'post',conn)

            response['message'] = 'Businesses Post successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Q1A Request failed, please try again later.')
        finally:
            disconnect(conn)

        # ENDPOINT AND JSON OBJECT THAT WORKS
        # http://localhost:4000/api/v2/businesses
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/businesses
        # {"business_id":"200-000001",
        #  "business_accepting_hours":
        #  "{\"Monday\":\"11:00am-12:00pm\",\"Tuesday\":\"10:00am-12:00pm\",\"Wednesday\":\"10:00am-12:00pm\",\"Thursday\":\"10:00am-12:00pm\",\"Friday\":\"10:00am-12:00pm\",\"Saturday\":\"10:00am-12:00pm\",\"Sunday\":\"10:00am-12:00pm\"}"}





# CUSTOMER QUERY 2
class ItemsbyBusiness(Resource):
    # RETURNS ALL ITEMS FOR A SPECIFIC BUSINESS
    def get(self, business_uid):
        response = {}
        items = {}
        print("business_uid", business_uid)
        try:
            conn = connect()
            query = """
                    SELECT * FROM sf.items 
                    WHERE itm_business_uid = \'""" + business_uid + """\'
                    """
            items = execute(query, 'get', conn)

            response['message'] = 'ItemsbyBusiness successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

        # http://localhost:4000/api/v2/itemsByBusiness/200-000003
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/itemsByBusiness/200-000003



# QUERY 3
# RETURNS ALL COUPON DETAILS FOR A SPECIFIC COUPON
class CouponDetails(Resource):
    def get(self, coupon_id):
        response = {}
        items = {}
        try:
            conn = connect()
            query = """
                    SELECT * FROM sf.coupons
                    WHERE coupon_id = \'""" + coupon_id + """\'
                    """
            items = execute(query, 'get', conn)

            response['message'] = 'CouponDetails successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

        # http://localhost:4000/api/v2/couponDetails/Jane6364
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/couponDetails/Jane6364


    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()
            data = request.get_json(force=True)

            coupon_uid = data['coupon_uid']
            num_used = (data['num_used'])
            print("coupon_uid", coupon_uid)
            print("num_used",  num_used)



            query = '''
                    UPDATE sf.coupons
                    SET num_used = \'''' + str(num_used) + '''\'
                    WHERE coupon_uid = \'''' + str(coupon_uid) + '''\';
                    '''
            items = execute(query,'post',conn)

            response['message'] = 'CouponDetails POST successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Q3 POST Request failed, please try again later.')
        finally:
            disconnect(conn)




# QUERY 8
# WRITES PURCHASE INFO TO PURCHASES AND PAYMENTS TABLES
class PurchaseData(Resource):
    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()
            data = request.get_json(force=True)
            # print to Received data to Terminal
            print("Received:", data)

            customer_uid = data['customer_uid']
            business_uid = data['business_uid']
            delivery_first_name = data['delivery_first_name']
            delivery_last_name = data['delivery_last_name']
            delivery_email = data['delivery_email']
            delivery_phone = data['delivery_phone']
            delivery_address = data['delivery_address']
            delivery_unit = data['delivery_unit']
            delivery_city = data['delivery_city']
            delivery_state = data['delivery_state']
            delivery_zip = data['delivery_zip']
            delivery_instructions = data['delivery_instructions']
            delivery_longitude = data['delivery_longitude']
            delivery_latitude = data['delivery_latitude']
            items = data['items']
            order_instructions = data['order_instructions']
            purchase_notes = data['purchase_notes']
            amount_due =  data['amount_due']
            amount_discount = data['amount_discount']
            amount_paid = data['amount_paid']

            print("customer_uid:", customer_uid)
            print("business_uid:", business_uid)

            print (business_uid )
            print (customer_uid )
            print (delivery_first_name )
            print (delivery_last_name )
            print (delivery_email )
            print (delivery_phone )
            print (delivery_address )
            print (delivery_unit )
            print (delivery_city )
            print (delivery_state )
            print (delivery_zip )
            print (delivery_instructions )
            print (delivery_longitude )
            print (delivery_latitude )
            print (items )
            print (order_instructions )
            print (purchase_notes )
            print (amount_due )
            print (amount_discount )
            print (amount_paid )

            # Query [0]  Get New Purchase UID
            query = ["CALL new_purchase_uid;"]
            NewPurIDresponse = execute(query[0], 'get', conn)
            NewPurID = NewPurIDresponse['result'][0]['new_id']
            print("NewPurID:", NewPurID)

            # Query [1]  Get New PaymentUID
            query = ["CALL new_payment_uid;"]
            NewPayIDresponse = execute(query[0], 'get', conn)
            NewPayID = NewPayIDresponse['result'][0]['new_id']
            print("NewPayID:", NewPayID)
            # print("NewID = ", NewID)  NewID is an Array and new_id is the first element in that array

            TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            DateStamp = datetime.now().strftime("%Y-%m-%d")
            print("TimeStamp:", TimeStamp)
            print("DateStamp:", DateStamp)

            # Query [2]  Main Query to Insert in Purchases Table
            query = '''
                    INSERT INTO  sf.purchases
                    SET purchase_uid = \'''' + NewPurID + '''\',
                        purchase_date = \'''' + TimeStamp + '''\',
                        purchase_id = \'''' + NewPurID + '''\',
                        pur_customer_uid = \'''' + customer_uid + '''\',
                        pur_business_uid = \'''' + business_uid + '''\',
                        delivery_first_name = \'''' + delivery_first_name + '''\',
                        delivery_last_name = \'''' + delivery_last_name + '''\',
                        delivery_email = \'''' + delivery_email + '''\',
                        delivery_phone_num = \'''' + delivery_phone + '''\',
                        delivery_address = \'''' + delivery_address + '''\',
                        delivery_unit = \'''' + delivery_unit + '''\',
                        delivery_city = \'''' + delivery_city + '''\',
                        delivery_state = \'''' + delivery_state + '''\',
                        delivery_zip = \'''' + delivery_zip + '''\',
                        delivery_instructions = \'''' + delivery_instructions + '''\',
                        delivery_longitude = \'''' + delivery_longitude + '''\',
                        delivery_latitude = \'''' + delivery_latitude + '''\',
                        items = \'''' + items + '''\',
                        order_instructions = \'''' + order_instructions + '''\',
                        purchase_notes = \'''' + purchase_notes + '''\';
                    '''

            items = execute(query,'post',conn)
            response['message'] = 'Purchase Data Post successful'

            # Query [3]  Main Query to Insert PaymentsTable
            query = '''
                    INSERT INTO sf.payments
                    SET payment_uid = \'''' + NewPayID + '''\',
                        payment_time_stamp = \'''' + TimeStamp + '''\',
                        payment_id = \'''' + NewPayID + '''\',
                        pay_purchase_id = \'''' + NewPurID + '''\',
                        amount_due = \'''' + amount_due + '''\',
                        amount_discount = \'''' + amount_discount+ '''\',
                        amount_paid = \'''' + amount_paid + '''\';
                        '''


            items = execute(query,'post',conn)
            response['message'] = 'Payment Data Post successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

        # ENDPOINT AND JSON OBJECT THAT WORKS
        # http://localhost:4000/api/v2/purchaseData
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/purchaseData
        # {  "customer_id":"4158329643",
        #    "business_id":"200-000003",
        #    "delivery_first_name":"Carlos",
        #    "delivery_last_name":"Torres",
        #    "delivery_email":"omarfacio2010@gmail.com",
        #    "delivery_phone":"4158329643",
        #    "delivery_address":"1658 Sacramento Street",
        #    "delivery_unit":"9",
        #    "delivery_city":"San Francisco",
        #    "delivery_state":"CA",
        #    "delivery_zip":"94109",
        #    "delivery_instructions":"Please dial 3434 to open the gate",
        #    "delivery_longitude":"37.000000",
        #    "delivery_latitude":"120.000000",
        #    "items":"{\"cilantro\": \"2\", \"potato\": \"4\", \"apple\": \"5\", \"melon\": \"1\", \"carrot\": \"2\"}",
        #    "order_instructions":"Please take care with my apples",
        #    "purchase_notes":"Repeat this order every Monday"
        # }



# QUERY 9 - QUANG'S QUERY
# PTYD WRITES PURCHASE INFO TO PURCHASES AND PAYMENTS TABLES
class MSPurchaseData(Resource):
    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()
            data = request.get_json(force=True)
            # print to Received data to Terminal
            print("Received:", data)

            customer_id = data['customer_id']
            business_id = data['business_id']
            delivery_first_name = data['delivery_first_name']
            delivery_last_name = data['delivery_last_name']
            delivery_email = data['delivery_email']
            delivery_phone = data['delivery_phone']
            delivery_address = data['delivery_address']
            delivery_unit = data['delivery_unit']
            delivery_city = data['delivery_city']
            delivery_state = data['delivery_state']
            delivery_zip = data['delivery_zip']
            delivery_instructions = data['delivery_instructions']
            delivery_longitude = data['delivery_longitude']
            delivery_latitude = data['delivery_latitude']
            items = data['items']
            order_instructions = data['order_instructions']
            purchase_notes = data['purchase_notes']
            amount_due =  data['amount_due']
            amount_discount = data['amount_discount']
            amount_paid = data['amount_paid']



            password_salt = data['salt']
            cc_num = data['cc_num']
            cc_exp_date = data['cc_exp_date']
            cc_cvv = data['cc_cvv']
            cc_zip = data['billing_zip']

            print("customer_id:", customer_id)
            print("business_id:", business_id)

            print (business_id )
            print (customer_id )
            print (delivery_first_name )
            print (delivery_last_name )
            print (delivery_email )
            print (delivery_phone )
            print (delivery_address )
            print (delivery_unit )
            print (delivery_city )
            print (delivery_state )
            print (delivery_zip )
            print (delivery_instructions )
            print (delivery_longitude )
            print (delivery_latitude )
            print (items )
            print (order_instructions )
            print (purchase_notes )
            print (amount_due )
            print (amount_discount )
            print (amount_paid )
            print (cc_num)
            print (cc_exp_date)
            print (cc_cvv)
            print (cc_zip)

            # Query [0]  Get New Purchase UID
            query = ["CALL new_purchase_uid;"]
            NewPurIDresponse = execute(query[0], 'get', conn)
            NewPurID = NewPurIDresponse['result'][0]['new_id']
            print("NewPurID:", NewPurID)

            # Query [1]  Get New PaymentUID
            query = ["CALL new_payment_uid;"]
            NewPayIDresponse = execute(query[0], 'get', conn)
            NewPayID = NewPayIDresponse['result'][0]['new_id']
            print("NewPayID:", NewPayID)
            # print("NewID = ", NewID)  NewID is an Array and new_id is the first element in that array

            TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            DateStamp = datetime.now().strftime("%Y-%m-%d")
            print("TimeStamp:", TimeStamp)
            print("DateStamp:", DateStamp)

            # Query [2]  Main Query to Insert in Purchases Table
            query = '''
                    INSERT INTO  sf.purchases
                    SET purchase_uid = new_purchase_id(),
                        purchase_date = \'''' + DateStamp + '''\',
                        purchase_id = \'''' + NewPurID + '''\',
                        customer_id = \'''' + customer_id + '''\',
                        business_id = \'''' + business_id + '''\',
                        delivery_first_name = \'''' + delivery_first_name + '''\',
                        delivery_last_name = \'''' + delivery_last_name + '''\',
                        delivery_email = \'''' + delivery_email + '''\',
                        delivery_phone_num = \'''' + delivery_phone + '''\',
                        delivery_address = \'''' + delivery_address + '''\',
                        delivery_unit = \'''' + delivery_unit + '''\',
                        delivery_city = \'''' + delivery_city + '''\',
                        delivery_state = \'''' + delivery_state + '''\',
                        delivery_zip = \'''' + delivery_zip + '''\',
                        delivery_instructions = \'''' + delivery_instructions + '''\',
                        delivery_longitude = \'''' + delivery_longitude + '''\',
                        delivery_latitude = \'''' + delivery_latitude + '''\',
                        items = \'''' + items + '''\',
                        order_instructions = \'''' + order_instructions + '''\',
                        purchase_notes = \'''' + purchase_notes + '''\';
                    '''

            items = execute(query,'post',conn)
            response['message'] = 'Purchase Data Post successful'

            # Query [3]  Main Query to Insert PaymentsTable
            query = '''
                    INSERT INTO sf.payments
                    SET payment_uid = \'''' + NewPayID + '''\',
                        payment_time_stamp = \'''' + TimeStamp + '''\',
                        payment_id = \'''' + NewPayID + '''\',
                        purchase_id = \'''' + NewPurID + '''\',
                        amount_due = \'''' + amount_due + '''\',
                        amount_discount = \'''' + amount_discount+ '''\',
                        amount_paid = \'''' + amount_paid + '''\',
                        cc_num = \'''' + cc_num + '''\', 
                        cc_exp_date = \'''' + cc_exp_date + '''\', 
                        cc_cvv = \'''' + cc_cvv + '''\', 
                        cc_zip = \'''' + cc_zip + '''\'
                        '''

            items = execute(query,'post',conn)
            response['message'] = 'Payment Data Post successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

        # ENDPOINT AND JSON OBJECT THAT WORKS
        # http://localhost:4000/api/v2/MSpurchaseData
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/MSpurchaseData
        #    {"customer_id":"100-000001",
        #     "business_id": "200-000001",
        #     "items": "320-000006",
        #     "amount_due" : "390.00",
        #     "salt": "64a7f1fb0df93d8f5b9df14077948afa1b75b4c5028d58326fb801d825c9cd24412f88c8b121c50ad5c62073c75d69f14557255da1a21e24b9183bc584efef71",
        #     "delivery_first_name":"Prashant",
        #     "delivery_last_name":"Marathay",
        #     "delivery_email":"pmarathay@gmail.com",
        #     "delivery_phone":"4084760001",
        #     "delivery_address":"6123 Corte De La Reina",
        #     "delivery_unit":"",
        #     "delivery_city":"San Jose",
        #     "delivery_state":"CA",
        #     "delivery_zip":"95120",
        #     "delivery_instructions":"Big Dog",
        #     "delivery_longitude":"-121.8891617",
        #     "delivery_latitude":",37.2271302",
        #     "order_instructions":"none",
        #     "purchase_notes":"none",
        #     "amount_discount":"0.00",
        #     "amount_paid":"300.00",
        #     "cc_num": "XXXXXXXXXXXX4242",
        #  	  "cc_exp_date":"2021-08-01",
        #     "cc_cvv":"123",
        #     "billing_zip":"12345"}

### CODE WRITTEN BY PARVA

class AccountSalt(Resource):
    def get(self, email):
        response = {}
        items = {}
        print("user email: ", email)
        try:
            conn = connect()
            query = """
                    SELECT password_algorithm, 
                            password_salt 
                    FROM sf.customers cus
                    WHERE customer_email = \'""" + email + """\';
                    """
            items = execute(query, 'get', conn)
            response['message'] = 'Login successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class Login(Resource):
    # input:api/v2/Login/annrupp22@gmail.com,4178980d28dcec5b36521c1a9beeef791db4e6674aa77,''"
    def get(self, email, password, refresh_token):
        response = {}
        items = []
        try:

            conn = connect()
            print(email, password, refresh_token)

            query = """ 
                    # CUSTOMER QUERY 1: LOGIN
                    SELECT customer_uid,
                            customer_last_name,
                            customer_first_name,
                            customer_email, 	
                            password_hashed, 	
                            email_verified, 	
                            user_social_media,
                            user_access_token,
                            user_refresh_token  
                    FROM sf.customers c 
                    -- WHERE customer_email = "1m4kfun@gmail.com";
                    WHERE customer_email = \'""" + email + """\';
                    """
            items = execute(query, 'get', conn)
            print('----------------- IN LOGIN ---------')
            print(items)
            if items['code'] == 480:
                response['message'] = "Internal Server Error."
                return response, 480
            elif not items['code']:
                response['message'] = 'Not Found'
                return response, 404
            else:
                print('in else')
                print(items['result'])
                print('sc: ', items['result'][0]['user_social_media'])
                if password is not None and items['result'][0]['user_social_media'] == 'TRUE':
                    response['message'] = "Need to login by Social Media"
                    return response, 401
                elif (password is None and refresh_token is None) or (password is None and items['result'][0]['user_social_media'] == 'FALSE'):
                    return BadRequest("Bad request.")
                # compare passwords if user_social_media is false
                elif (items['result'][0]['user_social_media'] == 'FALSE' or items['result'][0]['user_social_media'] == 'NULL') and password is not None:
                    print('IN ELIF')
                    print(items['result'][0]['password_hashed'])

                    if items['result'][0]['password_hashed'] != password:
                        response['message'] = "Wrong password."
                        return response, 401
                    if ((items['result'][0]['email_verified']) == '0') or (items['result'][0]['email_verified'] == "FALSE"):
                        response['message'] = "Account need to be verified by email."
                        return response, 401
                # compare the refresh token because it never expire.
                elif (items['result'][0]['user_social_media']) == 'TRUE':
                    if (items['result'][0]['user_refresh_token'] != refresh_token):
                        response['message'] = "Cannot Authenticated. Token is invalid."
                        return response, 401
                else:
                    string = " Cannot compare the password or refresh token while log in. "
                    print("*" * (len(string) + 10))
                    print(string.center(len(string) + 10, "*"))
                    print("*" * (len(string) + 10))
                    response['message'] = 'Internal Server Error.'
                    return response, 500

                del items['result'][0]['password_hashed']
                del items['result'][0]['email_verified']

                query = """
                    SELECT *
                    FROM sf.customers c
                    WHERE customer_email = \'""" + email + """\'
                    """
                items = execute(query, 'get', conn)

                response['message'] = "Authenticated success."
                response['result'] = items['result']
                return response, 200


        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class Profile(Resource):
    # Fetches ALL DETAILS FOR A SPECIFIC USER
    # INPUT EXAMPLE - api/v2/Login/XYZ@gmail.com
    def get(self, email):
        response = {}
        items = {}
        print("user_email: ", email)
        try:
            conn = connect()
            query = """
                    SELECT *
                    FROM sf.customers c
                    WHERE customer_email = \'""" + email + """\'
                    """
            items = execute(query, 'get', conn)

            response['message'] = 'Profile Loaded successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class History(Resource):
    # RETURNS PAST ORDERS FOR A SPECIFIC USER
    # INPUT EXAMPLE - api/v2/Login/XYZ@gmail.com
    def get(self, email):
        response = {}
        items = {}
        print("Email: ", email)
        try:
            conn = connect()
            query = """
                    SELECT *
                    FROM sf.customers c
                    WHERE customer_email = \'""" + email + """\'
                    """
            items = execute(query, 'get', conn)

            response['message'] = 'Profile Loaded successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class getItems(Resource):
    def get(self):
        response = {}
        items = {}

        try:
            conn = connect()
            query = """
                    SELECT it.*, bs.business_delivery_hours
                    FROM sf.items AS it, sf.businesses AS bs
                    WHERE it.itm_business_uid = bs.business_uid
                    """
            items = execute(query, 'get', conn)
            response['message'] = 'Items sent successfully'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

# updated refund
class Refund(Resource):
    # HTTP method POST
    # input example : {"image_url":"http://servingnow.me","email":"annrupp22@gmail.com","note":"Please issue a refund for carrots" }

    def post(self):
        response = {}
        items = []
        try:

            conn = connect()
            data = request.get_json(force=True)
            print(data)
            image_url = data['image_url']
            email = data['email']
            note = data['note']
            timeStamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            print('TIMESTAMP----------', timeStamp)
            query = ["CALL new_refund_uid;"]

            NewRefundIDresponse = execute(query[0], 'get', conn)
            NewRefundID = NewRefundIDresponse['result'][0]['new_id']
            print('refund id------', NewRefundIDresponse)

            customer_phone = execute("select customer_phone_num from sf.customers where customer_email =  \'" + email + "\';", 'get', conn)
            print('phone---', customer_phone)
            phone = customer_phone['result'][0]['customer_phone_num']
            print('completed')
            print("SELECT customer_email FROM sf.customers WHERE customer_email = \'" + email + "\';")

            query_email = ["SELECT customer_email FROM sf.customers WHERE customer_email = \'" + email + "\';"]
            query_insert = [""" INSERT INTO sf.refunds
                    (
                        refund_uid,
                        created_at,
                        email_id,
                        phone_num,
                        image_url,
                        customer_note
                    )

                    VALUES
                    (
                    \'""" + NewRefundID + """\'
                    , \'""" + timeStamp + """\'
                    , \'""" + email + """\'
                    , \'""" +  phone + """\'
                    , \'""" +  image_url + """\'
                    , \'""" + note + """\');"""]

            emailExists = execute(query_email[0], 'get', conn)
            print('email_exists', emailExists)
            if emailExists['result']:
                items = execute(query_insert[0], 'post', conn)
                statusCode = 200
                response['result'] = items
                response['message'] = 'Refund info generated'
            else:
                statusCode = 400
                response['result'] = 'Email does not exists'
                response['message'] = 'Email does not exists'
            return response, statusCode

        except:
            print("Error happened while generating refund ticket")
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)
            print('process completed')





# -- Queries end here -------------------------------------------------------------------------------

# Define API routes

api.add_resource(Businesses, '/api/v2/businesses')
api.add_resource(ItemsbyBusiness, '/api/v2/itemsByBusiness/<string:business_uid>')
api.add_resource(CouponDetails, '/api/v2/couponDetails/<string:coupon_id>', '/api/v2/couponDetails')
api.add_resource(PurchaseData, '/api/v2/purchaseData')


api.add_resource(AccountSalt, '/api/v2/AccountSalt/<string:email>')
api.add_resource(Login, '/api/v2/Login/<string:email>,<string:password>,<string:refresh_token>')
api.add_resource(Profile, '/api/v2/Profile/<string:email>')
api.add_resource(Refund, '/api/v2/Refund')
api.add_resource(getItems, '/api/v2/getItems')


api.add_resource(MSPurchaseData, '/api/v2/MSpurchaseData')

# Run on below IP address and port
# Make sure port number is unused (i.e. don't use numbers 0-1023)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)

