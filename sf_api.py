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
import pandas as pd
import io
import csv

from flask import Flask, request, render_template, redirect, url_for, make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_mail import Mail, Message
# used for serializer email and error handling
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
#from flask_cors import CORS

from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.security import generate_password_hash, check_password_hash

# Twilio settings
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')





#  NEED TO SOLVE THIS
from NotificationHub import Notification
from NotificationHub import NotificationHub
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
import jwt
s3 = boto3.client('s3')

# aws s3 bucket where the image is stored
BUCKET_NAME = os.environ.get('MEAL_IMAGES_BUCKET')
#BUCKET_NAME = 'servingnow'
# allowed extensions for uploading a profile photo file
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

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
stripe.api_key = stripe_secret_key


# Allow cross-origin resource sharing
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
app.config['DEBUG'] = True
# Adding for email testing
#app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_SERVER'] = 'smtp.mydomain.com'
app.config['MAIL_PORT'] = 465
#app.config['MAIL_USERNAME'] = 'ptydtesting@gmail.com'
#app.config['MAIL_PASSWORD'] = 'PTYDTesting1'
#app.config['MAIL_DEFAULT_SENDER'] = 'ptydtesting@gmail.com'
app.config['MAIL_USERNAME'] = 'support@servingfresh.me'
app.config['MAIL_PASSWORD'] = 'SupportFresh1'
app.config['MAIL_DEFAULT_SENDER'] = 'support@servingfresh.me'

app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

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

mail = Mail(app)
s = URLSafeTimedSerializer('thisisaverysecretkey')
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


# ===========================================================
# Additional Helper Functions from sf_api.py
# Need to revisit to see if we need these

def helper_upload_meal_img(file, key):
    bucket = 'servingfresh'
    if file and allowed_file(file.filename):
        filename = 'https://s3-us-west-1.amazonaws.com/' \
                   + str(bucket) + '/' + str(key)

        upload_file = s3.put_object(
                            Bucket=bucket,
                            Body=file,
                            Key=key,
                            ACL='public-read',
                            ContentType='image/jpeg'
                        )
        return filename
    return None

def helper_upload_refund_img(file, bucket, key):
    print("Bucket = ", bucket)
    print("Key = ", key)
    if file:
        filename = 'https://s3-us-west-1.amazonaws.com/' \
                   + str(bucket) + '/' + str(key)
        #print('bucket:{}'.format(bucket))
        upload_file = s3.put_object(
                            Bucket=bucket,
                            Body=file,
                            Key=key,
                            ACL='public-read',
                            ContentType='image/png'
                        )
        return filename
    return None

def allowed_file(filename):
    """Checks if the file is allowed to upload"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def kitchenExists(kitchen_id):
    # scan to check if the kitchen name exists
    kitchen = db.scan(TableName='kitchens',
        FilterExpression='kitchen_id = :val',
        ExpressionAttributeValues={
            ':val': {'S': kitchen_id}
        }
    )

    return not kitchen.get('Items') == []

def couponExists(coupon_id):
    # scan to check if the kitchen name exists
    coupon = db.scan(TableName='coupons',
        FilterExpression='coupon_id = :val',
        ExpressionAttributeValues={
            ':val': {'S': coupon_id}
        }
    )

    return not coupon.get('Items') == []


# ===========================================================

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

# QUERY 2A
class SubscriptionsbyBusiness(Resource):
    # RETURNS ALL SUBSCRIPTION ITEMS FOR A SPECIFIC BUSINESS
    def get(self, business_id):
        response = {}
        items = {}
        try:
            conn = connect()
            query = """
                    SELECT * FROM sf.subscription_items
                    WHERE itm_business_id = \'""" + business_id + """\'
                    """
            items = execute(query, 'get', conn)

            response['message'] = 'SubscriptionsbyBusiness successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

        # http://localhost:4000/api/v2/subscriptionsByBusiness/200-000001
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/subscriptionsByBusiness/200-000001





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


# QUERY 4
# WRITES REFUND INFO TO DB
class RefundDetails(Resource):
    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()
            data = request.get_json(force=True)
            # print to Received data to Terminal
            print("Received:", data)

            email = data['email_id']
            phone = data['phone_num']
            image = data['image_url']
            note = data['customer_note']
            print('email:', email)
            print('phone_num:', phone)
            print('image_url:', image)
            print('note:', note)


            # Query [0]  Get New Refund UID
            query = ["CALL new_refund_uid;"]
            NewIDresponse = execute(query[0], 'get', conn)
            NewID = NewIDresponse['result'][0]['new_id']
            # print("NewID = ", NewID)  NewID is an Array and new_id is the first element in that array
            print("NewRefundID = ", NewID)

            TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("TimeStamp = ", TimeStamp)

            #Query [1]  Main Query to Insert Data Into Table
            query =  '''
                    INSERT INTO  sf.refunds
                    SET refund_uid = \'''' + NewID + '''\',
                        created_at = \'''' + TimeStamp + '''\',
                        email_id = \'''' + email + '''\',
	                    phone_num = \'''' + phone + '''\',
	                    image_url = \'''' + image + '''\',
	                    customer_note = \'''' + note + '''\';
                    '''
            items = execute(query,'post',conn)

            response['message'] = 'RefundDetails Post successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

        # ENDPOINT AND JSON OBJECT THAT WORKS
        # http://localhost:4000/api/v2/refundDetails
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/refundDetails
            # {"email_id":"wmarathay@gmail.com",
            #  "phone_num":"408-476-0001",
            #  "image_url":"http://servingnow.me",
            #  "customer_note":"Please Refund"}


# QUERY 4 REWRITE TO MATCH HOWARD'S OUTPUT
# WRITES REFUND INFO TO DB
class RefundDetailsNEW(Resource):
    def post(self):
        response = {}
        items = {}

        try:
            conn = connect()
            client_email = request.form.get('client_email')
            client_message = request.form.get('client_message')
            client_phone = request.form.get('client_phone')
            # data = request.get_json(force=True)
            # print to Received data to Terminal
            # print("Received:", data)

            # email = data['client_email']
            # phone = data['phone_num']
            # image = data['image_url']
            # note = data['client_message']
            print('email:', client_email)
            # print('phone_num:', phone)
            # print('image_url:', image)
            print('note:', client_message)
            print('phone:', client_phone)


            # Query [0]  Get New Refund UID
            query = ["CALL new_refund_uid;"]
            NewIDresponse = execute(query[0], 'get', conn)
            NewID = NewIDresponse['result'][0]['new_id']
            # print("NewID = ", NewID)  NewID is an Array and new_id is the first element in that array
            print("NewRefundID = ", NewID)

            photo_key = 'refund_imgs/{}'.format(NewID)
            print("Photo Key = ", photo_key)

            print("Photo = ", photo)
            photo_path = helper_upload_refund_img(photo, BUCKET_NAME, photo_key)
            print("Photo Path = ", photo_path)



            TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("TimeStamp = ", TimeStamp)

            #Query [1]  Main Query to Insert Data Into Table
            query =  '''
                    INSERT INTO  sf.refunds
                    SET refund_uid = \'''' + NewID + '''\',
                        created_at = \'''' + TimeStamp + '''\',
                        email_id = \'''' + client_email + '''\',
	                    phone_num = \'''' + client_phone + '''\',
	                    image_url = \'''' + photo_path + '''\',
	                    customer_note = \'''' + client_message + '''\';
                    '''
            items = execute(query,'post',conn)

            response['message'] = 'RefundDetails Post successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
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
                        purchase_date = \'''' + TimeStamp + '''\',
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

####################### CODE WRITTEN BY PARVA ##############################

# -- Customer Queries Start here -------------------------------------------------------------------------------

class token_fetch_update (Resource):

    def post(self, action):
        items = {}
        try:
            conn = connect()
            data = request.get_json(force=True)
            uid = data['uid']
            print(data)

            if action == 'get':
                query = """
                        SELECT *
                        FROM sf.customers c
                        WHERE customer_uid = \'""" + uid + """\';
                        """
                items = execute(query, 'get', conn)

                if items['result']:

                    items['message'] = 'Tokens recieved successful'
                    items['result'] = items['result']
                    items['code'] = 200
                    return items
                else:
                    items['message'] = "UID doesn't exists"
                    items['result'] = items['result']
                    items['code'] = 404
                    return items

            elif action == 'update_mobile':
                query = """
                        UPDATE sf.customers 
                        SET  
                        mobile_access_token = \'""" + data['mobile_access_token'] + """\', 
                        mobile_refresh_token = \'""" + data['mobile_refresh_token'] + """\', 
                        social_timestamp = DATE_ADD(social_timestamp , INTERVAL 14 DAY)
                        WHERE customer_uid = \'""" + uid + """\';
                        """
                print(query)
                items = execute(query, 'post', conn)
                print(items)
                print('code------', items['code'])

                if items['code'] == 281:

                    items['message'] = 'Tokens and timestamp updated successful'
                    items['code'] = 200
                    return items
                else:
                    items['message'] = "UID doesn't exists"
                    items['result'] = items['result']
                    items['code'] = 404
                    return items

            elif action == 'update_web':
                query = """
                        UPDATE sf.customers 
                        SET  
                        user_access_token = \'""" + data['user_access_token'] + """\', 
                        user_refresh_token = \'""" + data['user_refresh_token'] + """\',
                        social_timestamp = DATE_ADD(social_timestamp , INTERVAL 14 DAY)
                        WHERE customer_uid = \'""" + uid + """\';
                        """
                print(query)
                items = execute(query, 'post', conn)
                print(items)
                print('code------', items['code'])

                if items['code'] == 281:

                    items['message'] = 'Tokens and timestamp updated successful'
                    items['code'] = 200
                    return items
                else:
                    items['message'] = "UID doesn't exists"
                    items['result'] = items['result']
                    items['code'] = 404
                    return items

            else:
                items['code'] = 400
                items['message'] = 'Select proper option'


        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class createAccount(Resource):
    def post(self):
        response = {}
        items = []
        try:
            conn = connect()
            data = request.get_json(force=True)
            print(data)
            email = data['email']
            firstName = data['first_name']
            lastName = data['last_name']
            phone = data['phone_number']
            address = data['address']
            unit = data['unit'] if data.get('unit') is not None else 'NULL'
            social_id = data['social_id'] if data.get('social_id') is not None else 'NULL'
            city = data['city']
            state = data['state']
            zip_code = data['zip_code']
            latitude = data['latitude']
            longitude = data['longitude']
            referral = data['referral_source']
            role = data['role']
            cust_id = data['cust_id'] if data.get('cust_id') is not None else 'NULL'

            if data.get('social') is None or data.get('social') == "FALSE" or data.get('social') == False or data.get('social') == 'NULL':
                social_signup = False
            else:
                social_signup = True

            print(social_signup)
            get_user_id_query = "CALL new_customer_uid();"
            NewUserIDresponse = execute(get_user_id_query, 'get', conn)

            if NewUserIDresponse['code'] == 490:
                string = " Cannot get new User id. "
                print("*" * (len(string) + 10))
                print(string.center(len(string) + 10, "*"))
                print("*" * (len(string) + 10))
                response['message'] = "Internal Server Error."
                return response, 500
            NewUserID = NewUserIDresponse['result'][0]['new_id']

            if social_signup == False:

                salt = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

                password = sha512((data['password'] + salt).encode()).hexdigest()
                print('password------', password)
                algorithm = "SHA512"
                mobile_access_token = 'NULL'
                mobile_refresh_token = 'NULL'
                user_access_token = 'NULL'
                user_refresh_token = 'NULL'
                user_social_signup = 'NULL'
            else:

                mobile_access_token = data['mobile_access_token']
                mobile_refresh_token = data['mobile_refresh_token']
                user_access_token = data['user_access_token']
                user_refresh_token = data['user_refresh_token']
                salt = 'NULL'
                password = 'NULL'
                algorithm = 'NULL'
                user_social_signup = data['social']

                print('ELSE- OUT')

            if cust_id != 'NULL' and cust_id:

                NewUserID = cust_id

                query = '''
                            SELECT user_access_token, user_refresh_token, mobile_access_token, mobile_refresh_token 
                            FROM sf.customers
                            WHERE customer_uid = \'''' + cust_id + '''\';
                       '''
                it = execute(query, 'get', conn)
                print('it-------', it)

                if it['result'][0]['user_access_token'] != 'FALSE':
                    user_access_token = it['result'][0]['user_access_token']

                if it['result'][0]['user_refresh_token'] != 'FALSE':
                    user_refresh_token = it['result'][0]['user_refresh_token']

                if it['result'][0]['mobile_access_token'] != 'FALSE':
                    mobile_access_token = it['result'][0]['mobile_access_token']

                if it['result'][0]['mobile_refresh_token'] != 'FALSE':
                    mobile_refresh_token = it['result'][0]['mobile_refresh_token']

                customer_insert_query =  ['''
                                    UPDATE sf.customers 
                                    SET 
                                    customer_created_at = \'''' + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + '''\',
                                    customer_first_name = \'''' + firstName + '''\',
                                    customer_last_name = \'''' + lastName + '''\',
                                    customer_phone_num = \'''' + phone + '''\',
                                    customer_address = \'''' + address + '''\',
                                    customer_unit = \'''' + unit + '''\',
                                    customer_city = \'''' + city + '''\',
                                    customer_state = \'''' + state + '''\',
                                    customer_zip = \'''' + zip_code + '''\',
                                    customer_lat = \'''' + latitude + '''\',
                                    customer_long = \'''' + longitude + '''\',
                                    password_salt = \'''' + salt + '''\',
                                    password_hashed = \'''' + password + '''\',
                                    password_algorithm = \'''' + algorithm + '''\',
                                    referral_source = \'''' + referral + '''\',
                                    role = \'''' + role + '''\',
                                    user_social_media = \'''' + user_social_signup + '''\',
                                    social_timestamp  =  DATE_ADD(now() , INTERVAL 14 DAY)
                                    WHERE customer_uid = \'''' + cust_id + '''\';
                                    ''']


            else:

                # check if there is a same customer_id existing
                query = """
                        SELECT customer_email FROM sf.customers
                        WHERE customer_email = \'""" + email + "\';"
                print('email---------')
                items = execute(query, 'get', conn)
                if items['result']:

                    items['result'] = ""
                    items['code'] = 409
                    items['message'] = "Email address has already been taken."

                    return items

                if items['code'] == 480:

                    items['result'] = ""
                    items['code'] = 480
                    items['message'] = "Internal Server Error."
                    return items


                # write everything to database
                customer_insert_query = ["""
                                        INSERT INTO sf.customers 
                                        (
                                            customer_uid,
                                            customer_created_at,
                                            customer_first_name,
                                            customer_last_name,
                                            customer_phone_num,
                                            customer_email,
                                            customer_address,
                                            customer_unit,
                                            customer_city,
                                            customer_state,
                                            customer_zip,
                                            customer_lat,
                                            customer_long,
                                            password_salt,
                                            password_hashed,
                                            password_algorithm,
                                            referral_source,
                                            role,
                                            user_social_media,
                                            user_access_token,
                                            social_timestamp,
                                            user_refresh_token,
                                            mobile_access_token,
                                            mobile_refresh_token,
                                            social_id
                                        )
                                        VALUES
                                        (
                                        
                                            \'""" + NewUserID + """\',
                                            \'""" + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + """\',
                                            \'""" + firstName + """\',
                                            \'""" + lastName + """\',
                                            \'""" + phone + """\',
                                            \'""" + email + """\',
                                            \'""" + address + """\',
                                            \'""" + unit + """\',
                                            \'""" + city + """\',
                                            \'""" + state + """\',
                                            \'""" + zip_code + """\',
                                            \'""" + latitude + """\',
                                            \'""" + longitude + """\',
                                            \'""" + salt + """\',
                                            \'""" + password + """\',
                                            \'""" + algorithm + """\',
                                            \'""" + referral + """\',
                                            \'""" + role + """\',
                                            \'""" + user_social_signup + """\',
                                            \'""" + user_access_token + """\',
                                            DATE_ADD(now() , INTERVAL 14 DAY),
                                            \'""" + user_refresh_token + """\',
                                            \'""" + mobile_access_token + """\',
                                            \'""" + mobile_refresh_token + """\',
                                            \'""" + social_id + """\');"""]
            print(customer_insert_query[0])
            items = execute(customer_insert_query[0], 'post', conn)

            if items['code'] != 281:
                items['result'] = ""
                items['code'] = 480
                items['message'] = "Error while inserting values in database"

                return items


            items['result'] = {
                'first_name': firstName,
                'last_name': lastName,
                'customer_uid': NewUserID,
                'access_token': user_access_token,
                'refresh_token': user_refresh_token,
                'access_token': mobile_access_token,
                'refresh_token': mobile_refresh_token,
                'social_id': social_id


            }
            items['message'] = 'Signup successful'
            items['code'] = 200

            print('sss-----', social_signup)
            return items

        except:
            print("Error happened while Sign Up")
            if "NewUserID" in locals():
                execute("""DELETE FROM customers WHERE customer_uid = '""" + NewUserID + """';""", 'post', conn)
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class email_verification(Resource):
    def post(self):

        try:
            conn = connect()

            data = request.get_json(force=True)
            print(data)
            email = data['email']
            query = """
                    SELECT password_hashed
                    FROM sf.customers c
                    WHERE customer_email = \'""" + email + """\'
                    """
            items = execute(query, 'get', conn)
            print(items)
            if not items['result']:

                items['message'] = "Customer email doesn't exists"
                items['code'] = 404
                return items
            if items['result'][0]['password_hashed'] == '':
                items['message'] = "Customer password doesn't exists"
                items['code'] = 405
                return items

            token = s.dumps(email)
            print(token)
            password = items['result'][0]['password_hashed']
            print(password)
            msg = Message("Email Verification", sender='support@servingfresh.me', recipients=[email])

            print('MESSAGE----', msg)
            print('message complete')
            link = url_for('confirm', token=token, hashed=password, _external=True)
            print('link---', link)
            #msg.body = "Click on the link {} to verify your email address.".format(link)

            msg.body = "Congratulations for signing up with Serving Fresh!\n\n" \
                       "Please click on the link below to be redirected to our website. " \
                       "Email support@servingfresh.me if you run into any problems or have any questions.\n" \
                       "Thx - The Serving Fresh Team\n\n" \
                       "{}".format(link)

            print('msg-bd----', msg.body)
            mail.send(msg)
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)




# confirmation page
@app.route('/api/v2/confirm', methods=['GET'])
def confirm():
    try:
        token = request.args['token']
        hashed = request.args['hashed']
        print("hased: ", hashed)
        email = s.loads(token)  # max_age = 86400 = 1 day

        # marking email confirmed in database, then...
        conn = connect()
        query = """UPDATE customers SET email_verified = 1 WHERE customer_email = \'""" + email + """\';"""
        update = execute(query, 'post', conn)
        if update.get('code') == 281:
            # redirect to login page
            # only for testing on localhost
            #return redirect('http://localhost:3000/login?email={}&hashed={}'.format(email, hashed))
            return redirect('https://servingfresh.me/login?email={}&hashed={}'.format(email, hashed))
        else:
            print("Error happened while confirming an email address.")
            error = "Confirm error."
            err_code = 401  # Verification code is incorrect
            return error, err_code
    except (SignatureExpired, BadTimeSignature) as err:
        status = 403  # forbidden
        return str(err), status
    finally:
        disconnect(conn)


class AccountSalt(Resource):
    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()

            data = request.get_json(force=True)
            print(data)
            email = data['email']
            query = """
                    SELECT password_algorithm, 
                            password_salt,
                            user_social_media 
                    FROM sf.customers cus
                    WHERE customer_email = \'""" + email + """\';
                    """
            items = execute(query, 'get', conn)
            print(items)
            if not items['result']:
                items['message'] = "Email doesn't exists"
                items['code'] = 404
                return items
            if items['result'][0]['user_social_media'] != 'NULL':
                items['message'] = """Social Signup exists. Use \'""" + items['result'][0]['user_social_media'] + """\' """
                items['code'] = 401
                return items
            items['message'] = 'SALT sent successfully'
            items['code'] = 200
            return items
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class Login(Resource):
    def post(self):
        response = {}
        try:
            conn = connect()
            data = request.get_json(force=True)
            email = data['email']
            password = data.get('password')
            social_id = data.get('social_id')
            signup_platform = data.get('signup_platform')
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
                        user_refresh_token,
                        user_access_token,
                        user_refresh_token,
                        social_id
                    FROM sf.customers c
                    WHERE customer_email = \'""" + email + """\';
                    """
            items = execute(query, 'get', conn)
            print('Password', password)
            print(items)

            if items['code'] != 280:
                response['message'] = "Internal Server Error."
                response['code'] = 500
                return response
            elif not items['result']:
                items['message'] = 'Email Not Found. Please signup'
                items['result'] = ''
                items['code'] = 404
                return items
            else:
                print(items['result'])
                print('sc: ', items['result'][0]['user_social_media'])


                # checks if login was by social media
                if password and items['result'][0]['user_social_media'] != 'NULL' and items['result'][0]['user_social_media'] != None:
                    response['message'] = "Need to login by Social Media"
                    response['code'] = 401
                    return response

               # nothing to check
                elif (password is None and social_id is None) or (password is None and items['result'][0]['user_social_media'] == 'NULL'):
                    response['message'] = "Enter password else login from social media"
                    response['code'] = 405
                    return response

                # compare passwords if user_social_media is false
                elif (items['result'][0]['user_social_media'] == 'NULL' or items['result'][0]['user_social_media'] == None) and password is not None:

                    if items['result'][0]['password_hashed'] != password:
                        items['message'] = "Wrong password"
                        items['result'] = ''
                        items['code'] = 406
                        return items

                    if ((items['result'][0]['email_verified']) == '0') or (items['result'][0]['email_verified'] == "FALSE"):
                        response['message'] = "Account need to be verified by email."
                        response['code'] = 407
                        return response

                # compare the social_id because it never expire.
                elif (items['result'][0]['user_social_media']) != 'NULL':

                    if signup_platform != items['result'][0]['user_social_media']:
                        items['message'] = "Wrong social media used for signup. Use \'" + items['result'][0]['user_social_media'] + "\'."
                        items['result'] = ''
                        items['code'] = 411
                        return items

                    if (items['result'][0]['social_id'] != social_id):
                        print(items['result'][0]['social_id'])

                        items['message'] = "Cannot Authenticated. Social_id is invalid"
                        items['result'] = ''
                        items['code'] = 408
                        return items

                else:
                    string = " Cannot compare the password or social_id while log in. "
                    print("*" * (len(string) + 10))
                    print(string.center(len(string) + 10, "*"))
                    print("*" * (len(string) + 10))
                    response['message'] = string
                    response['code'] = 500
                    return response
                del items['result'][0]['password_hashed']
                del items['result'][0]['email_verified']

                query = "SELECT * from sf.customers WHERE customer_email = \'" + email + "\';"
                items = execute(query, 'get', conn)
                items['message'] = "Authenticated successfully."
                items['code'] = 200
                return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class AppleLogin (Resource):

    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()
            token = request.form.get('id_token')
            access_token = request.form.get('code')
            print(token)
            if token:
                print('INN')
                data = jwt.decode(token, verify=False)
                print('data-----', data)
                email = data.get('email')

                print(data, email)
                if email is not None:
                    sub = data['sub']
                    query = """
                    SELECT customer_uid,
                        customer_last_name,
                        customer_first_name,
                        customer_email,
                        password_hashed,
                        email_verified,
                        user_social_media,
                        user_access_token,
                        user_refresh_token,
                        social_id
                    FROM sf.customers c
                    WHERE social_id = \'""" + sub + """\';
                    """
                    items = execute(query, 'get', conn)
                    print(items)

                    if items['code'] != 280:
                        items['message'] = "Internal error"
                        return items


                    # new customer


                    if not items['result']:
                        print('New customer')
                        items['message'] = "Social_id doesn't exists Please go to the signup page"
                        get_user_id_query = "CALL new_customer_uid();"
                        NewUserIDresponse = execute(get_user_id_query, 'get', conn)

                        if NewUserIDresponse['code'] == 490:
                            string = " Cannot get new User id. "
                            print("*" * (len(string) + 10))
                            print(string.center(len(string) + 10, "*"))
                            print("*" * (len(string) + 10))
                            response['message'] = "Internal Server Error."
                            response['code'] = 500
                            return response

                        NewUserID = NewUserIDresponse['result'][0]['new_id']
                        user_social_signup = 'APPLE'
                        print('NewUserID', NewUserID)


                        customer_insert_query = """
                                    INSERT INTO sf.customers 
                                    (
                                        customer_uid,
                                        customer_created_at,
                                        customer_email,
                                        user_social_media,
                                        user_refresh_token,
                                        user_access_token,
                                        social_id,
                                        social_timestamp
                                    )
                                    VALUES
                                    (
                                    
                                        \'""" + NewUserID + """\',
                                        \'""" + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + """\',
                                        \'""" + email + """\',
                                        \'""" + user_social_signup + """\',
                                        \'""" + access_token + """\',
                                        \'""" + access_token + """\',
                                        \'""" + sub + """\',
                                        DATE_ADD(now() , INTERVAL 1 DAY)
                                    );"""

                        item = execute(customer_insert_query, 'post', conn)

                        print('INSERT')

                        if item['code'] != 281:
                            item['message'] = 'Check insert sql query'
                            return item
                        print('successful redirect to signup')
                        return redirect("https://servingfresh.me/socialsignup?id=" + NewUserID)


                    # Existing customer

                    print('existing-------')
                    print(items['result'][0]['user_social_media'])
                    print(items['result'][0]['social_id'])

                    if items['result'][0]['user_social_media'] != "APPLE":
                        print('1-----')
                        items['message'] = "Wrong social media used for signup. Use \'" + items['result'][0]['user_social_media'] + "\'."
                        items['code'] = 400
                        return redirect("https://servingfresh.me/?media=" + items['result'][0]['user_social_media'])

                    elif items['result'][0]['social_id'] != sub:
                        print('20-----')
                        items['message'] = "social_id mismatch"
                        items['code'] = 400
                        return redirect("https://servingfresh.me/")

                    else:
                        print('successful redirect to farms')
                        return redirect("https://servingfresh.me/?id=" + items['result'][0]['customer_uid'])



                else:
                    items['message'] = "Social_id not returned by Apple LOGIN"
                    items['code'] = 400
                    return items


            else:
                response = {
                    "message": "Token not found in Apple's Response",
                    "code": 400
                }
                return response
        except:
            raise BadRequest("Request failed, please try again later.")

class access_refresh_update(Resource):

    def post(self):

        try:
            conn = connect()
            data = request.get_json(force=True)
            query = """
                    UPDATE sf.customers SET user_access_token = \'""" + data['access_token'] + """\', user_refresh_token = \'""" + data['refresh_token'] + """\', social_timestamp =  \'""" + data['social_timestamp'] + """\' WHERE (customer_uid = \'""" + data['uid'] + """\'); ;
                    """
            print(query)
            items = execute(query, 'post', conn)
            if items['code'] == 281:
                items['message'] = 'Access and refresh token updated successfully'
                print(items['code'])
                items['code'] = 200
            else:
                items['message'] = 'Check sql query'
                items['code'] = 400
            return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class Profile(Resource):
    # Fetches ALL DETAILS FOR A SPECIFIC USER

    def get(self, id):
        response = {}
        items = {}
        try:
            conn = connect()
            query = """
                    SELECT *
                    FROM sf.customers c
                    WHERE customer_uid = \'""" + id + """\'
                    """
            items = execute(query, 'get', conn)

            if items['result']:

                items['message'] = 'Profile Loaded successful'
                items['result'] = items['result']
                items['code'] = 200
                return items
            else:
                items['message'] = "Customer UID doesn't exists"
                items['result'] = items['result']
                items['code'] = 404
                return items
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class update_Profile(Resource):

    def post(self):
        response = {}
        items = {}
        try:
            data = request.get_json(force=True)
            conn = connect()

            query = """
                    UPDATE  sf.customers  
                    SET  
                    customer_first_name  = \'""" + data['customer_first_name'] + """\',  
                    customer_last_name  =  '""" + data['customer_last_name'] + """',  
                    customer_phone_num  =  '""" + data['customer_phone_num'] + """',  
                    customer_email  =  '""" + data['customer_email'] + """',  
                    customer_address  =  '""" + data['customer_address'] + """',  
                    customer_unit  =  '""" + data['customer_unit'] + """',  
                    customer_city  =  '""" + data['customer_city'] + """',  
                    customer_state  =  '""" + data['customer_state'] + """',  
                    customer_zip  =  '""" + data['customer_zip'] + """',  
                    customer_lat  =  '""" + data['customer_lat'] + """',  
                    customer_long  =  '""" + data['customer_long'] + """' 
                    WHERE ( customer_uid  = '""" + data['customer_uid'] + """' );
                    """
            items = execute(query, 'post', conn)
            if items['code'] == 281:
                items['message'] = 'customer info updated successfully'
                return items
            else:
                items['message'] = 'check sql query'
                return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class update_email_password(Resource):

    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()
            data = request.get_json(force=True)

            query = """
                    SELECT *
                    FROM sf.customers c
                    WHERE customer_uid = \'""" + data['customer_uid'] + """\'
                    """
            items = execute(query, 'get', conn)

            if not items['result']:

                items['message'] = "Customer UID doesn't exists"
                items['result'] = items['result']
                items['code'] = 404
                return items

            salt = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            password = sha512((data['password'] + salt).encode()).hexdigest()

            query = """
                        UPDATE  sf.customers  
                        SET  
                        customer_email  =  '""" + data['customer_email'] + """',  
                        password_salt  =  '""" + salt + """',  
                        password_hashed  =  '""" + password + """'
                        WHERE ( customer_uid  = '""" + data['customer_uid'] + """' );
                        """

            items = execute(query, 'post', conn)
            if items['code'] == 281:
                items['message'] = 'customer email and password updated successfully'
                return items
            else:
                items['message'] = 'check sql query'
                return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class update_guid_notification(Resource):

    def post(self, role, action):
        response = {}
        items = {}

        try:
            conn = connect()
            data = request.get_json(force=True)

            print(data)
            if role == 'customer' and action == 'add':
                uid = data['uid']
                guid = data['guid']
                notification = data['notification']
                query = """
                        SELECT *
                        FROM sf.customers c
                        WHERE customer_uid = \'""" + uid + """\'
                        """
                items = execute(query, 'get', conn)
                del data['uid']
                test = str(data).replace("'", "\"")
                print('test---------', test)
                data = "'" + test + "'"

                print(data)
                if items['result']:

                    query = " " \
                            "UPDATE sf.customers " \
                            "SET cust_guid_device_id_notification  = (SELECT JSON_MERGE_PRESERVE(cust_guid_device_id_notification," + data + ")) " \
                            "WHERE customer_uid = '" + str(uid) + "';" \
                            ""

                    items = execute(query, 'post', conn)
                    print(items)
                    if items['code'] == 281:
                        items['code'] = 200
                        items['message'] = 'Device_id notification and GUID updated'
                    else:
                        items['message'] = 'check sql query'

                else:
                    items['message'] = "UID doesn't exists"

                return items

            elif role == 'business' and action == 'add':
                uid = data['uid']
                guid = data['guid']
                query = """
                        SELECT *
                        FROM sf.businesses b
                        WHERE business_uid = \'""" + uid + """\'
                        """
                items = execute(query, 'get', conn)

                del data['uid']
                test = str(data).replace("'", "\"")
                print('test---------', test)
                data = "'" + test + "'"

                if items['result']:
                    data
                    query = " " \
                            "UPDATE sf.businesses " \
                            "SET bus_guid_device_id_notification  = (SELECT JSON_MERGE_PRESERVE(bus_guid_device_id_notification," + data + ")) " \
                            "WHERE business_uid = '" + str(uid) + "';" \
                            ""

                    items = execute(query, 'post', conn)

                    if items['code'] == 281:
                        items['code'] = 200
                        items['message'] = 'Device_id notification and GUID updated'
                    else:
                        items['message'] = 'check sql query'

                else:
                    items['message'] = "UID doesn't exists"

                return items

            #GUIDS

            elif role == 'customer' and action == 'update':
                query = """
                    SELECT cust_guid_device_id_notification
                    FROM sf.customers c
                    WHERE customer_uid = \'""" + data['uid'] + """\';
                    """
                items = execute(query, 'get', conn)
                json_guid = json.loads(items['result'][0]['cust_guid_device_id_notification'])
                for i, vals in enumerate(json_guid):
                    print(i, vals)
                    if vals == None or vals == 'null':
                        continue
                    if vals['guid'] == data['guid']:
                        print(vals)
                        json_guid[i]['notification'] = data['notification']
                        break
                if json_guid[0] == None:
                    json_guid[0] = 'null'

                guid = str(json_guid)
                guid = guid.replace("'", '"')
                print(guid)
                query = """
                        UPDATE  sf.customers  
                        SET
                        cust_guid_device_id_notification = \'""" + guid + """\'
                        WHERE ( customer_uid  = '""" + data['uid'] + """' );
                        """
                items = execute(query, 'post', conn)
                if items['code'] != 281:
                    items['message'] = 'guid not updated check sql query and data'

                else:
                    items['message'] = 'guid updated'
                return items

            elif role == 'business' and action == 'update':
                query = """
                    SELECT bus_guid_device_id_notification
                    FROM sf.businesses b
                    WHERE business_uid = \'""" + data['uid'] + """\';
                    """
                items = execute(query, 'get', conn)
                json_guid = json.loads(items['result'][0]['bus_guid_device_id_notification'])
                for i, vals in enumerate(json_guid):
                    print(i, vals)
                    if vals == None or vals == 'null':
                        continue
                    if vals['guid'] == data['guid']:
                        print(vals)
                        json_guid[i]['notification'] = data['notification']
                        break
                if json_guid[0] == None:
                    json_guid[0] = 'null'

                guid = str(json_guid)
                guid = guid.replace("'", '"')
                print(guid)
                query = """
                        UPDATE  sf.businesses
                        SET
                        bus_guid_device_id_notification = \'""" + guid + """\'
                        WHERE ( business_uid  = '""" + data['uid'] + """' );
                        """
                items = execute(query, 'post', conn)
                if items['code'] != 281:
                    items['message'] = 'guid not updated check sql query and data'

                else:
                    items['message'] = 'guid updated'
                return items

            else:
                return 'choose correct option'

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class categoricalOptions(Resource):
    def get(self, long, lat):
        response = {}
        items = {}

        try:
            conn = connect()

            # query for businesses serving in customer's zone
            query = """
                    SELECT zone
                    FROM
                    (SELECT *,  
                    IF (
                    IF ((z.LT_lat - z.LB_lat)/(z.LT_long - z.LB_long) <= 0,
                    \'""" + lat + """\' >=  (z.LT_lat - z.LB_lat)/(z.LT_long - z.LB_long) * \'""" + long + """\' + z.LT_lat - z.LT_long * (z.LT_lat - z.LB_lat)/(z.LT_long - z.LB_long),
                    \'""" + lat + """\' <=   (z.LT_lat - z.LB_lat)/(z.LT_long - z.LB_long) * \'""" + long + """\' + z.LT_lat - z.LT_long * (z.LT_lat - z.LB_lat)/(z.LT_long - z.LB_long)) AND
                           
                    \'""" + lat + """\' <= (z.RT_lat - z.LT_lat)/(z.RT_long - z.LT_long) * \'""" + long + """\' + z.RT_lat - z.RT_long * (z.RT_lat - z.LT_lat)/(z.RT_long - z.LT_long) AND
                           
                    IF ((z.RB_lat - z.RT_lat)/(z.RB_long - z.RT_long) >= 0,  
                    \'""" + lat + """\' >= (z.RB_lat - z.RT_lat)/(z.RB_long - z.RT_long) * \'""" + long + """\' + z.RB_lat - z.RB_long * (z.RB_lat - z.RT_lat)/(z.RB_long - z.RT_long),
                    \'""" + lat + """\' <= (z.RB_lat - z.RT_lat)/(z.RB_long - z.RT_long) * \'""" + long + """\' + z.RB_lat - z.RB_long * (z.RB_lat - z.RT_lat)/(z.RB_long - z.RT_long)) AND
                           
                    \'""" + lat + """\' >= (z.LB_lat - z.RB_lat)/(z.LB_long - z.RB_long) * \'""" + long + """\' + z.LB_lat - z.LB_long * (z.LB_lat - z.RB_lat)/(z.LB_long - z.RB_long), "TRUE", "FALSE") AS "In_Zone",
                     
                    FORMAT((z.LT_lat - z.LB_lat)/(z.LT_long - z.LB_long),3) AS "LEFT_SLOPE",
                    FORMAT((z.RB_lat - z.RT_lat)/(z.RB_long - z.RT_long),3) AS "RIGHT_SLOPE"
                    FROM sf.zones z) AS DD
                    WHERE In_Zone = 'True'
                    ;
                    """
            items = execute(query, 'get', conn)
            if items['code'] != 280:
                items['message'] = 'check sql query'
                return items
            zones = []
            for vals in items['result']:
                zones.append(vals['zone'])
            print('ZONES-----', zones)
            query = """
                    SELECT      
                    rjzjt.zone_uid,
                    rjzjt.zone,
                    rjzjt.zone_name,
                    rjzjt.z_id,
                    rjzjt.z_biz_id,
                    rjzjt.z_delivery_day,
                    b.business_name,
                    rjzjt.z_delivery_day,
                    rjzjt.z_delivery_time,
                    rjzjt.LB_long,rjzjt.LB_lat,rjzjt.LT_long,rjzjt.LT_lat,rjzjt.RT_long,rjzjt.RT_lat,rjzjt.RB_long,rjzjt.RB_lat,
                    b.business_type,
                    b.business_image
                   
                FROM sf.businesses b
                RIGHT JOIN
                (SELECT *
                     FROM sf.zones AS z,
                     json_table(z_businesses, '$[*]'
                         COLUMNS (
                                z_id FOR ORDINALITY,
                                z_biz_id VARCHAR(255) PATH '$')
                                             ) as zjt) as rjzjt
                ON b.business_uid = rjzjt.z_biz_id
                WHERE zone IN """ + str(tuple(zones)) + """;
                """
            items = execute(query, 'get', conn)

            if items['code'] != 280:
                items['message'] = 'check sql query'
            return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class getItems(Resource):
    def post(self):
        response = {}
        items = {}

        try:
            conn = connect()

            data = request.get_json(force=True)
            ids = data['ids']
            type = data['type']
            type.append('Random')
            type.append('Random2')
            ids.append('Random')
            ids.append('Random2')

            query = """
                    SELECT * 
                    FROM sf.items
                    WHERE item_type IN """ + str(tuple(type)) + """ AND itm_business_uid IN """ + str(tuple(ids)) + """
                    ORDER BY item_name;
                    """
            print(query)
            items = execute(query, 'get', conn)

            if items['code'] != 280:
                items['message'] = 'check sql query'
                return items

            items['message'] = 'Items sent successfully'
            items['code'] = 200
            """
            # get max profit

            dict_items = {}
            rm_idx = []
            result = items['result']
            print('RESULT-----------')
            print(result[0])
            for i, vals in enumerate(result):
                if vals['item_name'] + vals["item_type"] + vals["item_unit"] in dict_items.keys():
                    if dict_items[vals['item_name'] + vals["item_type"] + vals["item_unit"]][0] < vals["item_price"] - vals["business_price"]:
                        rm_idx.append(dict_items[vals['item_name'] + vals["item_type"] + vals["item_unit"]][1])
                        dict_items[vals['item_name'] + vals["item_type"] + vals["item_unit"]] = [vals["item_price"] - vals["business_price"], i]
                    else:
                        rm_idx.append(i)
                else:
                    dict_items[vals['item_name'] + vals["item_type"] + vals["item_unit"]] = [vals["item_price"] - vals["business_price"], i]

            print('VALS---------')
            print(dict_items)
            print(rm_idx)

            for dd in rm_idx:
                print(result[dd])

            result = [i for j, i in enumerate(result) if j not in rm_idx]

            items['result'] = result
            """
            return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

# updated refund
class Refund(Resource):
    # HTTP method POST

    def post(self):
        response = {}
        items = []
        try:
            #dtdt
            conn = connect()

            email = request.form.get('email')
            note = request.form.get('note')
            item_photo = request.files.get('item_photo')
            timeStamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

            query = ["CALL new_refund_uid;"]

            NewRefundIDresponse = execute(query[0], 'get', conn)
            NewRefundID = NewRefundIDresponse['result'][0]['new_id']
            print('INN')
            query = """
                    SELECT customer_phone_num FROM sf.customers 
                    WHERE customer_email = \'""" + str(email) + """\';
                    """
            items = execute(query, 'get', conn)
            print(items)

            if not items['result']:

                items['result'] = email
                items['message'] = 'Email does not exists'
                items['code'] = 400

                return items

            ## add photo

            key = "refund/" + NewRefundID
            print(key)
            item_photo_url = helper_upload_meal_img(item_photo, key)
            print(item_photo_url)

            phone = items['result'][0]['customer_phone_num']
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
                            , \'""" + phone + """\'
                            , \'""" + item_photo_url + """\'
                            , \'""" + note.replace("'", "") + """\');"""
                            ]

            emailExists = execute(query_email[0], 'get', conn)
            print('email_exists', emailExists)
            items = execute(query_insert[0], 'post', conn)
            print(items)
            if items['code'] != 281:
                items['message'] = 'check sql query and input'
                return items
            else:
                items['code'] = 200
                items['message'] = 'Refund info generated'
                return items

        except:
            print("Error happened while generating refund ticket")
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)
            print('process completed')


class available_Coupons(Resource):
    def get(self, email):
        response = {}
        items = []
        try:
            conn = connect()

            if email == 'guest':
                email = ''

            query = """
                    SELECT *
                    FROM sf.coupons
                    WHERE (email_id = \'""" + email + """\' OR email_id = '') AND limits > num_used AND expire_date> CURDATE();;
                    """
            items = execute(query, 'get', conn)
            items['message'] = 'Coupons sent successfully'
            items['code'] = 200
            return items
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class purchase(Resource):
    def post(self):
            response = {}
            items = {}
            try:
                conn = connect()
                data = request.get_json(force=True)

                query = "CALL sf.new_purchase_uid"
                newPurchaseUID_query = execute(query, 'get', conn)
                newPurchaseUID = newPurchaseUID_query['result'][0]['new_id']

                purchase_uid = newPurchaseUID
                purchase_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                purchase_id = purchase_uid
                purchase_status = 'ACTIVE'
                pur_customer_uid = data['pur_customer_uid']
                pur_business_uid = data['pur_business_uid']
                items_pur = data['items']
                order_instructions = data['order_instructions']
                delivery_instructions = data['delivery_instructions']
                order_type = data['order_type']
                delivery_first_name = data['delivery_first_name']
                delivery_last_name = data['delivery_last_name']
                delivery_phone_num = data['delivery_phone_num']
                delivery_email = data['delivery_email']
                delivery_address = data['delivery_address']
                delivery_unit = data['delivery_unit']
                delivery_city = data['delivery_city']
                delivery_state = data['delivery_state']
                delivery_zip = data['delivery_zip']
                delivery_latitude = data['delivery_latitude']
                delivery_longitude = data['delivery_longitude']
                purchase_notes = data['purchase_notes']

                query = "SELECT * FROM sf.customers " \
                        "WHERE customer_email =\'"+delivery_email+"\';"

                items = execute(query, 'get', conn)

                print('ITEMS--------------', items)

                if not items['result']:
                    items['code'] = 404
                    items['message'] = "User email doesn't exists"
                    return items

                print('in insert-------')

                query_insert = """ 
                                    INSERT INTO sf.purchases
                                    SET
                                    purchase_uid = \'""" + newPurchaseUID + """\',
                                    purchase_date = \'""" + purchase_date + """\',
                                    purchase_id = \'""" + purchase_id + """\',
                                    purchase_status = \'""" + purchase_status + """\',
                                    pur_customer_uid = \'""" + pur_customer_uid + """\',
                                    pur_business_uid = \'""" + pur_business_uid + """\',
                                    items = \'""" + items_pur + """\',
                                    order_instructions = \'""" + order_instructions + """\',
                                    delivery_instructions = \'""" + delivery_instructions + """\',
                                    order_type = \'""" + order_type + """\',
                                    delivery_first_name = \'""" + delivery_first_name + """\',
                                    delivery_last_name = \'""" + delivery_last_name + """\',
                                    delivery_phone_num = \'""" + delivery_phone_num + """\',
                                    delivery_email = \'""" + delivery_email + """\',
                                    delivery_address = \'""" + delivery_address + """\',
                                    delivery_unit = \'""" + delivery_unit + """\',
                                    delivery_city = \'""" + delivery_city + """\',
                                    delivery_state = \'""" + delivery_state + """\',
                                    delivery_zip = \'""" + delivery_zip + """\',
                                    delivery_latitude = \'""" + delivery_latitude + """\',
                                    delivery_longitude = \'""" + delivery_longitude + """\',
                                    purchase_notes = \'""" + purchase_notes + """\';
                                """


                #print(query_insert)
                items = execute(query_insert, 'post', conn)

                print('execute')
                if items['code'] == 281:
                    items['code'] = 200
                    items['message'] = 'Purchase info updated'

                else:
                    items['message'] = 'check sql query'
                    items['code'] = 490

                items['result'] = newPurchaseUID
                return items

            except:
                print("Error happened while inserting in purchase table")

                raise BadRequest('Request failed, please try again later.')
            finally:
                disconnect(conn)


class payment(Resource):
    def post(self):
            response = {}
            item = {}
            try:
                conn = connect()
                data = request.get_json(force=True)

                query = "CALL sf.new_payment_uid"
                newPaymentUID_query = execute(query, 'get', conn)
                newPaymentUID = newPaymentUID_query['result'][0]['new_id']

                payment_uid = newPaymentUID
                payment_id = payment_uid
                pay_purchase_uid = data['pay_purchase_uid']
                pay_purchase_id = data['pay_purchase_id']
                payment_time_stamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                start_delivery_date = data['start_delivery_date']
                pay_coupon_id = data['pay_coupon_id']
                amount_due = data['amount_due']
                amount_discount = data['amount_discount']
                amount_paid = data['amount_paid']
                info_is_Addon = data['info_is_Addon']
                cc_num = data['cc_num']
                cc_exp_date = data['cc_exp_date']
                cc_cvv = data['cc_cvv']
                cc_zip = data['cc_zip']
                charge_id = data['charge_id']
                payment_type = data['payment_type']
                print(data)

                query_insert = [""" 
                                    INSERT INTO  sf.payments
                                    SET
                                    payment_uid = \'""" + payment_uid + """\',
                                    payment_id = \'""" + payment_id + """\',
                                    pay_purchase_uid = \'""" + pay_purchase_uid + """\',
                                    pay_purchase_id = \'""" + pay_purchase_id + """\',
                                    payment_time_stamp = \'""" + payment_time_stamp + """\',
                                    start_delivery_date = \'""" + start_delivery_date + """\',
                                    pay_coupon_id = \'""" + pay_coupon_id + """\',
                                    amount_due = \'""" + amount_due + """\',
                                    amount_discount = \'""" + amount_discount + """\',
                                    amount_paid = \'""" + amount_paid + """\',
                                    info_is_Addon = \'""" + info_is_Addon + """\',
                                    cc_num = \'""" + cc_num + """\',
                                    cc_exp_date = \'""" + cc_exp_date + """\',
                                    cc_cvv = \'""" + cc_cvv + """\',
                                    cc_zip = \'""" + cc_zip + """\',
                                    charge_id = \'""" + charge_id + """\',
                                    payment_type = \'""" + payment_type + """\';
                                    
                                """]


                print(query_insert)
                item = execute(query_insert[0], 'post', conn)

                if item['code'] == 281:
                    item['code'] = 200
                    item['message'] = 'Payment info updated'
                else:
                    item['message'] = 'check sql query'
                    item['code'] = 490

                return item

            except:
                print("Error happened while inserting in payments table")
                raise BadRequest('Request failed, please try again later.')
            finally:
                disconnect(conn)
                print('process completed')


class get_Fee_Tax(Resource):
    def get(self, z_id, day):
        try:
            conn = connect()
            query = """
                    SELECT service_fee, tax_rate, delivery_fee, z_delivery_time AS delivery_time
                    FROM sf.zones
                    WHERE zone = \'""" + z_id + """\' AND z_delivery_day = \'""" + day + """\';
                    """
            items = execute(query, 'get', conn)
            if items['code'] != 280:
                items['message'] = 'Check sql query'
                return items
            items['result'] = items['result'][0]
            return items
        except:
                print("Error happened while getting taxes")
                raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)
            print('process completed')


class purchase_Data_SF(Resource):
    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()
            data = request.get_json(force=True)

            # Purchases start here

            query = "CALL sf.new_purchase_uid"
            newPurchaseUID_query = execute(query, 'get', conn)
            newPurchaseUID = newPurchaseUID_query['result'][0]['new_id']

            purchase_uid = newPurchaseUID
            purchase_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            purchase_id = purchase_uid
            purchase_status = 'ACTIVE'
            pur_customer_uid = data['pur_customer_uid']
            pur_business_uid = data['pur_business_uid']
            #items_pur = data['items']
            items_pur = "'[" + ", ".join([str(val).replace("'", "\"") if val else "NULL" for val in data['items']]) + "]'"
            order_instructions = data['order_instructions']
            delivery_instructions = data['delivery_instructions']
            order_type = data['order_type']
            delivery_first_name = data['delivery_first_name']
            delivery_last_name = data['delivery_last_name']
            delivery_phone_num = data['delivery_phone_num']
            delivery_email = data['delivery_email']
            delivery_address = data['delivery_address']
            delivery_unit = data['delivery_unit']
            delivery_city = data['delivery_city']
            delivery_state = data['delivery_state']
            delivery_zip = data['delivery_zip']
            delivery_latitude = data['delivery_latitude']
            delivery_longitude = data['delivery_longitude']
            delivery_status = data['delivery_status'] if data.get('delivery_status') is not None else 'FALSE'
            purchase_notes = data['purchase_notes']

            """
            query = "SELECT * FROM sf.customers " \
                    "WHERE customer_email =\'"+delivery_email+"\';"

            items = execute(query, 'get', conn)

            print('ITEMS--------------', items)

            if not items['result']:
                items['code'] = 404
                items['message'] = "User email doesn't exists"
                return items
            """
            print('in insert-------')

            query_insert = """ 
                                INSERT INTO sf.purchases
                                SET
                                purchase_uid = \'""" + newPurchaseUID + """\',
                                purchase_date = \'""" + purchase_date + """\',
                                purchase_id = \'""" + purchase_id + """\',
                                purchase_status = \'""" + purchase_status + """\',
                                pur_customer_uid = \'""" + pur_customer_uid + """\',
                                pur_business_uid = \'""" + pur_business_uid + """\',
                                items = """ + items_pur + """,
                                order_instructions = \'""" + order_instructions + """\',
                                delivery_instructions = \'""" + delivery_instructions + """\',
                                order_type = \'""" + order_type + """\',
                                delivery_first_name = \'""" + delivery_first_name + """\',
                                delivery_last_name = \'""" + delivery_last_name + """\',
                                delivery_phone_num = \'""" + delivery_phone_num + """\',
                                delivery_email = \'""" + delivery_email + """\',
                                delivery_address = \'""" + delivery_address + """\',
                                delivery_unit = \'""" + delivery_unit + """\',
                                delivery_city = \'""" + delivery_city + """\',
                                delivery_state = \'""" + delivery_state + """\',
                                delivery_zip = \'""" + delivery_zip + """\',
                                delivery_latitude = \'""" + delivery_latitude + """\',
                                delivery_longitude = \'""" + delivery_longitude + """\',
                                purchase_notes = \'""" + purchase_notes + """\',
                                delivery_status = \'""" + delivery_status + """\';
                            """
            items = execute(query_insert, 'post', conn)

            print('execute')
            if items['code'] == 281:
                items['code'] = 200
                items['message'] = 'Purchase info updated'

            else:
                items['message'] = 'check sql query'
                items['code'] = 490


            # Payments start here


            query = "CALL sf.new_payment_uid"
            newPaymentUID_query = execute(query, 'get', conn)
            newPaymentUID = newPaymentUID_query['result'][0]['new_id']

            payment_uid = newPaymentUID
            payment_id = payment_uid
            pay_purchase_uid = newPurchaseUID
            pay_purchase_id = newPurchaseUID
            payment_time_stamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            start_delivery_date = data['start_delivery_date']
            pay_coupon_id = data['pay_coupon_id']
            amount_due = data['amount_due']
            amount_discount = data['amount_discount']
            amount_paid = data['amount_paid']
            info_is_Addon = data['info_is_Addon']
            cc_num = data['cc_num']
            cc_exp_date = data['cc_exp_date']
            cc_cvv = data['cc_cvv']
            cc_zip = data['cc_zip']
            charge_id = data['charge_id']
            payment_type = data['payment_type']
            print("data------")
            print(data)

            query_insert = [""" 
                                INSERT INTO  sf.payments
                                SET
                                payment_uid = \'""" + payment_uid + """\',
                                payment_id = \'""" + payment_id + """\',
                                pay_purchase_uid = \'""" + pay_purchase_uid + """\',
                                pay_purchase_id = \'""" + pay_purchase_id + """\',
                                payment_time_stamp = \'""" + payment_time_stamp + """\',
                                start_delivery_date = \'""" + start_delivery_date + """\',
                                pay_coupon_id = \'""" + pay_coupon_id + """\',
                                amount_due = \'""" + amount_due + """\',
                                amount_discount = \'""" + amount_discount + """\',
                                amount_paid = \'""" + amount_paid + """\',
                                info_is_Addon = \'""" + info_is_Addon + """\',
                                cc_num = \'""" + cc_num + """\',
                                cc_exp_date = \'""" + cc_exp_date + """\',
                                cc_cvv = \'""" + cc_cvv + """\',
                                cc_zip = \'""" + cc_zip + """\',
                                charge_id = \'""" + charge_id + """\',
                                payment_type = \'""" + payment_type + """\';
                                
                            """]

            print(query_insert)
            item = execute(query_insert[0], 'post', conn)
            print(item)

            if item['code'] == 281:
                item['code'] = 200
                item['message'] = 'Payment info updated'
            else:
                item['message'] = 'check sql query'
                item['code'] = 490
                return items
            print('coupons')
            if pay_coupon_id:
                print('IN coupons')
                query = """
                    SELECT *
                    FROM sf.coupons
                    WHERE coupon_uid = \'""" + pay_coupon_id + """\';
                    """

                items = execute(query, 'get', conn)
                if not items['result']:
                    items['message'] = "Coupon uid doesn't exists"
                    items['code'] = 404
                    return items

                query = """
                        UPDATE sf.coupons SET num_used = num_used + 1 WHERE (coupon_uid = \'""" + pay_coupon_id + """\');
                        """
                items = execute(query, 'post', conn)
                items['message'] = 'purchase, payments and coupons info updated'
                items['code'] = 200
            return items

        except:
            print("Error happened while inserting in purchase table")

            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class history(Resource):
    # Fetches ALL DETAILS FOR A SPECIFIC USER

    def get(self, uid):
        response = {}
        items = {}
        print("user_uid: ", uid)
        try:
            conn = connect()
            query = """
                    SELECT * 
                    FROM sf.purchases as pur, sf.payments as pay
                    WHERE pur.purchase_uid = pay.pay_purchase_uid AND pur.pur_customer_uid = \'""" + uid + """\'
                    ORDER BY pur.purchase_date DESC; 
                    """
            items = execute(query, 'get', conn)

            items['message'] = 'History Loaded successful'
            items['code'] = 200
            return items
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class Stripe_Intent(Resource):
    def post(self):
        response = {}


        if request.form.get('amount') == None:
            raise BadRequest('Request failed. Please provide the amount field.')
        try:
            amount = int(float(request.form.get('amount')) * 100)
        except:
            raise BadRequest('Request failed. Unable to convert amount to int')
        print('AMOUNT------', amount)

        intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='usd',
        )
        print('INTENT------', intent)
        client_secret = intent.client_secret
        intent_id = intent.id
        response['client_secret'] = client_secret
        response['id'] = intent_id
        response['code'] = 200
        print(response['client_secret'])
        print(response['id'])
        return response

class Stripe_Payment_key_checker(Resource):
    def post(self):
        response = {}
        data = request.get_json(force=True)
        key_test = "pk_test_6RSoSd9tJgB2fN2hGkEDHCXp00MQdrK3Tw"
        key_live = "pk_live_g0VCt4AW6k7tyjRw61O3ac5a00Tefdbp8E"

        if data['key'] == key_test:
            # if app is in testing
            stripe_status = "Test"
            # if app is live
            #stripe_status = "Live"
            return stripe_status

        elif data['key'] == key_live:
            # if app is in testing
            stripe_status = "Test"
            # if app is live
            #stripe_status = "Live"
            return stripe_status

        else:
            return 200
        return response


class Paypal_Payment_key_checker(Resource):
    def post(self):
        response = {}
        data = request.get_json(force=True)
        key_test = "Acg-SnCe4XqkDEjd2YmVgphGr_y9o_BPWkov-kp_TP6dpD6jPIg9M8Ltm8t6xog-Ym0dFMcHCbsVCSHD"
        key_live = "Abg89Ka2pj3KK7TEujTgFKdMcY_v-JSo6rQmyucgcDl7rgrLoMCsNwZNiChk4wuCLDnfl3OO_dF7iB1F"

        if data['key'] == key_test:
            # if app is in testing
            paypal_status = 'Test'
            # if app is live
            #paypal_status = 'Live'
            return paypal_status

        elif data['key'] == key_live:
            # if app is in testing
            paypal_status = 'Test'
            # if app is live
            #paypal_status = 'Live'
            return paypal_status

        else:
            return 200
        return response


# -- Customer Queries End here -------------------------------------------------------------------------------

# -- Farmers Queries Start here -------------------------------------------------------------------------------

class addItems(Resource):
    def post(self, action):

        items = {}
        try:
            conn = connect()

            if action == 'Insert':
                itm_business_uid = request.form.get('itm_business_uid')
                item_name = request.form.get('item_name') if request.form.get('item_name') is not None else 'NULL'
                item_status = request.form.get('item_status') if request.form.get('item_status') is not None else 'NULL'
                item_type = request.form.get('item_type') if request.form.get('item_type') is not None else 'NULL'
                item_desc = request.form.get('item_desc') if request.form.get('item_desc') is not None else 'NULL'
                item_unit = request.form.get('item_unit') if request.form.get('item_unit') is not None else 'NULL'
                item_price = request.form.get('item_price') if request.form.get('item_price') is not None else 'NULL'
                business_price = request.form.get('business_price') if request.form.get('business_price') is not None else 'NULL'
                item_sizes = request.form.get('item_sizes') if request.form.get('item_sizes') is not None else 'NULL'
                favorite = request.form.get('favorite') if request.form.get('favorite') is not None else 'NULL'
                item_photo = request.files.get('item_photo')
                exp_date = request.form.get('exp_date') if request.form.get('exp_date') is not None else 'NULL'
                taxable = request.form.get('taxable') if request.form.get('taxable') is not None else 'NULL'
                print('IN')

                query = ["CALL sf.new_items_uid;"]
                NewIDresponse = execute(query[0], 'get', conn)
                NewID = NewIDresponse['result'][0]['new_id']
                key = "items/" + NewID
                print(key)
                item_photo_url = helper_upload_meal_img(item_photo, key)
                print(item_photo_url)
                print("NewRefundID = ", NewID)
                TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("TimeStamp = ", TimeStamp)

                # INSERT query
                query_insert =  '''
                                INSERT INTO sf.items
                                SET 
                                itm_business_uid = \'''' + itm_business_uid + '''\',
                                item_name = \'''' + item_name + '''\',
                                item_status = \'''' + item_status + '''\',
                                item_type = \'''' + item_type + '''\',
                                item_desc = \'''' + item_desc + '''\',
                                item_unit = \'''' + item_unit + '''\',
                                item_price = \'''' + item_price + '''\',
                                business_price = \'''' + business_price + '''\',
                                item_sizes = \'''' + item_sizes + '''\',
                                favorite = \'''' + favorite + '''\',
                                item_photo = \'''' + item_photo_url + '''\',
                                exp_date = \'''' + exp_date + '''\',
                                created_at = \'''' + TimeStamp + '''\',
                                taxable = \'''' + taxable + '''\',
                                item_uid = \'''' + NewID + '''\';
                                '''
                items = execute(query_insert, 'post', conn)
                print(items)

                if items['code'] == 281:
                    items['message'] = 'Item added successfully'
                    items['code'] = 200
                else:
                    items['message'] = 'check sql query'
                    items['code'] = 490
                return items

            elif action == 'Update':
                # Update query

                item_uid = request.form.get('item_uid')
                itm_business_uid = request.form.get('itm_business_uid')
                item_name = request.form.get('item_name')
                item_status = request.form.get('item_status')
                item_type = request.form.get('item_type')
                item_desc = request.form.get('item_desc')
                item_unit = request.form.get('item_unit')
                item_price = request.form.get('item_price')
                item_sizes = request.form.get('item_sizes')
                favorite = request.form.get('favorite')
                taxable = request.form.get('taxable')
                business_price = request.form.get('business_price') if request.form.get('business_price') is not None else 'NULL'
                print('In')
                item_photo = request.files.get('item_photo') if request.files.get('item_photo') is not None else 'NULL'
                print('oout')
                exp_date = request.form.get('exp_date')
                key = "items/" + str(item_uid)


                if item_photo == 'NULL':
                    print('IFFFFF------')

                    query_update =  '''
                                    UPDATE sf.items
                                    SET 
                                    itm_business_uid = \'''' + itm_business_uid + '''\',
                                    item_name = \'''' + item_name + '''\',
                                    item_status = \'''' + item_status + '''\',
                                    item_type = \'''' + item_type + '''\',
                                    item_desc = \'''' + item_desc + '''\',
                                    item_unit = \'''' + item_unit + '''\',
                                    item_price = \'''' + item_price + '''\',
                                    business_price = \'''' + business_price + '''\',
                                    item_sizes = \'''' + item_sizes + '''\',
                                    favorite = \'''' + favorite + '''\',
                                    taxable = \'''' + taxable + '''\',
                                    exp_date = \'''' + exp_date + '''\'
                                    WHERE item_uid = \'''' + item_uid + '''\';
                                '''
                else:
                    print('ELSE--------')
                    item_photo_url = helper_upload_meal_img(item_photo, key)
                    query_update =  '''
                                    UPDATE sf.items
                                    SET 
                                    itm_business_uid = \'''' + itm_business_uid + '''\',
                                    item_name = \'''' + item_name + '''\',
                                    item_status = \'''' + item_status + '''\',
                                    item_type = \'''' + item_type + '''\',
                                    item_desc = \'''' + item_desc + '''\',
                                    item_unit = \'''' + item_unit + '''\',
                                    item_price = \'''' + item_price + '''\',
                                    business_price = \'''' + business_price + '''\',
                                    item_sizes = \'''' + item_sizes + '''\',
                                    favorite = \'''' + favorite + '''\',
                                    taxable = \'''' + taxable + '''\',
                                    item_photo = \'''' + item_photo_url + '''\',
                                    exp_date = \'''' + exp_date + '''\'
                                    WHERE item_uid = \'''' + item_uid + '''\';
                                '''

                items = execute(query_update, 'post', conn)
                print(items)

                if items['code'] == 281:
                    items['message'] = 'Item updated successfully'
                    items['code'] = 200
                else:
                    items['message'] = 'check sql query'
                    items['code'] = 490
                return items

            else:

                # Update item_status
                print('ELSE-------------')
                item_uid = request.form.get('item_uid')
                item_status = request.form.get('item_status')
                query_status =  '''
                                UPDATE sf.items
                                SET 
                                item_status = \'''' + item_status + '''\'
                                WHERE item_uid = \'''' + item_uid + '''\';
                                '''
                items = execute(query_status, 'post', conn)
                print(items)

                if items['code'] == 281:
                    items['message'] = 'Item updated successfully'
                    items['code'] = 200
                else:
                    items['message'] = 'check sql query'
                    items['code'] = 490
                return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class all_businesses(Resource):

    def get(self):
        try:
            conn = connect()

            query = """
                    SELECT business_uid, business_name FROM sf.businesses; 
                    """
            items = execute(query, 'get', conn)
            if items['code'] == 280:
                items['message'] = 'Business data returned successfully'
                items['code'] = 200
            else:
                items['message'] = 'Check sql query'
            print(items)
            return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class business_details_update(Resource):
    def post(self, action):
            try:
                conn = connect()
                data = request.get_json(force=True)

                if action == 'Get':
                    query = "SELECT * FROM sf.businesses WHERE business_uid = \'" + data['business_uid'] + "\';"
                    item = execute(query, 'get', conn)
                    if item['code'] == 280:
                        if not item['result']:
                            item['message'] = 'No such business uid exists'
                        else:
                            item['message'] = 'Business table loaded successfully'
                        item['code'] = 200
                    else:
                        item['message'] = 'check sql query'
                        item['code'] = 490
                    return item
                else:
                    print("IN ELSE")
                    print(data)
                    print('IN')


                    business_association = str(data['business_association'])
                    business_association = "'" + business_association.replace("'", "\"") + "'"
                    business_hours = str(data['business_hours'])
                    business_hours = "'" + business_hours.replace("'", "\"") + "'"
                    business_accepting_hours = str(data['business_accepting_hours'])
                    business_accepting_hours = "'" + business_accepting_hours.replace("'", "\"") + "'"
                    business_delivery_hours = str(data['business_delivery_hours'])
                    business_delivery_hours = "'" + business_delivery_hours.replace("'", "\"") + "'"
                    print('OUT')
                    query = """
                               UPDATE sf.businesses
                               SET 
                               business_created_at = \'""" + data["business_created_at"] + """\',
                               business_name = \'""" + data["business_name"] + """\',
                               business_type = \'""" + data["business_type"] + """\',
                               business_desc = \'""" + data["business_desc"] + """\',
                               business_association = """ + business_association + """,
                               business_contact_first_name = \'""" + data["business_contact_first_name"] + """\',
                               business_contact_last_name = \'""" + data["business_contact_last_name"] + """\',
                               business_phone_num = \'""" + data["business_phone_num"] + """\',
                               business_phone_num2 = \'""" + data["business_phone_num2"] + """\',
                               business_email = \'""" + data["business_email"] + """\',
                               business_hours = """ + business_hours + """,
                               business_accepting_hours = """ + business_accepting_hours + """,
                               business_delivery_hours = """ + business_delivery_hours + """,
                               business_address = \'""" + data["business_address"] + """\',
                               business_unit = \'""" + data["business_unit"] + """\',
                               business_city = \'""" + data["business_city"] + """\',
                               business_state = \'""" + data["business_state"] + """\',
                               business_zip = \'""" + data["business_zip"] + """\',
                               business_longitude = \'""" + data["business_longitude"] + """\',
                               business_latitude = \'""" + data["business_latitude"] + """\',
                               business_EIN = \'""" + data["business_EIN"] + """\',
                               business_WAUBI = \'""" + data["business_WAUBI"] + """\',
                               business_license = \'""" + data["business_license"] + """\',
                               business_USDOT = \'""" + data["business_USDOT"] + """\',
                               bus_notification_approval = \'""" + data["bus_notification_approval"] + """\',
                               can_cancel = \'""" + data["can_cancel"] + """\',
                               delivery = \'""" + data["delivery"] + """\',
                               reusable = \'""" + data["reusable"] + """\',
                               business_image = \'""" + data["business_image"] + """\',
                               business_password = \'""" + data["business_password"] + """\',
                               platform_fee = \'""" + data["platform_fee"] + """\',
                               transaction_fee = \'""" + data["transaction_fee"] + """\',
                               revenue_sharing = \'""" + data["revenue_sharing"] + """\',
                               profit_sharing = \'""" + data["profit_sharing"] + """\'
                               WHERE business_uid = \'""" + data["business_uid"] + """\' ;
                             """
                    print(query)
                    item = execute(query, 'post', conn)
                    print(item)
                    if item['code'] == 281:
                        item['code'] = 200
                        item['message'] = 'Business info updated'
                    else:
                        item['message'] = 'check sql query'
                        item['code'] = 490
                    return item

            except:
                print("Error happened while outputting from business table")
                raise BadRequest('Request failed, please try again later.')
            finally:
                disconnect(conn)
                print('process completed')

class orders_by_farm(Resource):

    def get(self):

        try:
            conn = connect()
            query = """
                    SELECT * FROM sf.orders_by_farm; 
                    """
            items = execute(query, 'get', conn)
            if items['code'] == 280:
                items['message'] = 'Orders by farm view loaded successful'
                items['code'] = 200
            else:
                items['message'] = 'Check sql query'


            df = pd.DataFrame.from_dict(items['result'])

            query = """
                    SELECT business_uid, business_name FROM sf.businesses; 
                    """
            items_bus = execute(query, 'get', conn)
            if items_bus['code'] == 280:
                items_bus['message'] = 'Business data returned successfully'
                items_bus['code'] = 200
            else:
                items_bus['message'] = 'Check sql query'
            print(items_bus)
            data = items_bus['result']
            bus_dict = {}
            for vals in data:
                bus_dict[vals["business_uid"]] = vals["business_name"]


            print(df.itm_business_uid.unique())
            bus_uids = df.itm_business_uid.unique()
            for ids in bus_uids:
                print(ids)
                if ids == None:
                    continue
                df_bus = df[df.itm_business_uid == ids]
                df_bus.sort_values(by=['name'], inplace=True)

                if ids in bus_dict:
                    path = "business_" + bus_dict[ids] + "_" + ids + ".csv"
                else:
                    path = "business_uid_" + ids + ".csv"
                #df_bus.to_csv(path)
                slider_output = df_bus.to_csv()

            #df.to_csv ('export_dataframe.csv', index = False, header=True)



            output = make_response(slider_output)
            output.headers["Content-Disposition"] = "attachment; filename=orders.csv"
            output.headers["Content-type"] = "text/csv"
            return output
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class orders_info(Resource):

    def get(self):

        try:
            conn = connect()

            query = """
                    SELECT pur.*, pay.amount_due, pay.amount_paid  
                    FROM sf.purchases as pur, sf.payments as pay
                    WHERE pur.purchase_uid = pay.pay_purchase_uid;
                    """
            items = execute(query, 'get', conn)
            if items['code'] == 280:
                items['message'] = 'Orders view loaded successful'
                items['code'] = 200
            else:
                items['message'] = 'Check sql query'
            return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class orderSummary(Resource):

    def get(self):
        try:
            conn = connect()
            query = """
                    SELECT obf.*, SUM(obf.qty) AS total_qty, SUM(obf.price) AS total_price, pay.start_delivery_date, pay.payment_uid 
                    FROM sf.orders_by_farm AS obf, sf.payments AS pay
                    WHERE obf.purchase_uid = pay.pay_purchase_uid AND pay.start_delivery_date >= CURDATE()
                    GROUP BY  obf.delivery_address, obf.delivery_unit, obf.delivery_city, obf.delivery_state, obf.delivery_zip, obf.item_uid;
                    """
            items = execute(query, 'get', conn)
            if items['code'] != 280:
                items['message'] = 'check sql query'

            return items
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class order_actions(Resource):

    def post(self, action):

        try:
            conn = connect()
            data = request.get_json(force=True)
            purchase_uid = data['purchase_uid'] if data.get('purchase_uid') is not None else 'NULL'
            if action == 'Delete':
                print('IN DELETE')

                purchase_uid = data['purchase_uid'] if data.get('purchase_uid') is not None else 'NULL'

                if purchase_uid == 'NULL':
                    return 'UID Incorrect'

                query_pur = """
                        DELETE FROM sf.purchases WHERE (purchase_uid = \'""" + purchase_uid + """\');
                        """
                item = execute(query_pur, 'post', conn)
                if item['code'] == 281:
                    item['message'] = 'Order deleted'
                    item['code'] = 200
                else:
                    item['message'] = 'Check sql query'

                query_pay = """
                        DELETE FROM sf.payments WHERE (pay_purchase_uid = \'""" + purchase_uid + """\');
                        """
                item = execute(query_pay, 'post', conn)
                if item['code'] == 281:
                    item['message'] = 'order deleted successful'
                    item['code'] = 200
                else:
                    item['message'] = 'Check sql query'

            elif action == 'delivery_status_YES':
                print('DELIVERY_YES')

                query = """
                        UPDATE sf.purchases 
                        SET delivery_status = 'Yes' 
                        WHERE purchase_uid = \'""" + purchase_uid + """\';
                        """
                print(query)
                item = execute(query, 'post', conn)
                print(item)

                if item['code'] == 281:
                    item['code'] = 200
                    item['message'] = 'Delivery Status updated'
                else:
                    item['message'] = 'check sql query'
                    item['code'] = 490

            elif action == 'delivery_status_NO':

                print('DELIVERY_NO')
                query = """
                        UPDATE sf.purchases 
                        SET delivery_status = 'No' 
                        WHERE purchase_uid = \'""" + purchase_uid + """\';
                        """

                item = execute(query, 'post', conn)

                if item['code'] == 281:
                    item['code'] = 200
                    item['message'] = 'Delivery Status updated'
                else:
                    item['message'] = 'check sql query'
                    item['code'] = 490

            elif action == 'item_delete':
                print('item_delete')
                #itm = str(data['item_data'])
                itm = json.dumps(data['item_data'])
                print(itm)
                itm = "'[" + ", ".join([str(val).replace("'", "\"") if val else "NULL" for val in data['item_data']]) + "]'"

                query = """ 
                        UPDATE sf.purchases 
                        SET 
                        items = """ + itm + """
                        WHERE (purchase_uid = \'""" + purchase_uid + """\');
                        """
                print(query)
                item = execute(query, 'post', conn)
                print(item)

                if item['code'] == 281:
                    item['code'] = 200
                    item['message'] = 'items deleted updated'
                else:
                    item['message'] = 'check sql query'
                    item['code'] = 490

            else:
                return 'Select proper option'

            return item

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)



class update_all_items(Resource):

    def post(self, uid):

        try:
            conn = connect()
            query = """
                    UPDATE sf.items
                    SET item_status = 'Active'
                    WHERE itm_business_uid = \'""" + uid + """\';
                    """
            items = execute(query, 'post', conn)
            if items['code'] == 281:
                items['message'] = 'items status updated successfully'
                items['code'] = 200
            else:
                items['message'] = 'Check sql query'
            return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class get_item_photos(Resource):

    def post(self, category):

        try:
            conn = connect()
            data = request.get_json(force=True)
            uid = data['uid']
            result = []
            if category == 'item':
                query = """
                        SELECT item_photo FROM sf.items WHERE item_uid = \'""" + uid + """\';
                        """
            elif category == 'business':
                query = """
                        SELECT item_photo FROM sf.items WHERE itm_business_uid = \'""" + uid + """\';
                        """
            else:
                return 'choose correct option'
            items = execute(query, 'get', conn)
            if items['code'] == 280:
                for vals in items['result']:
                    result.append(vals['item_photo'])
                items['result'] = result
                items['message'] = 'Photos loaded successful'
                items['code'] = 200
            else:
                items['message'] = 'Check sql query'
            return items
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class update_Coupons(Resource):
    def post(self, action):
            response = {}
            items = []
            try:
                #coupon_uid
                conn = connect()
                data = request.get_json(force=True)

                if action == 'create':

                    query = ["CALL sf.new_coupons_uid;"]
                    couponIDresponse = execute(query[0], 'get', conn)
                    couponID = couponIDresponse['result'][0]['new_id']

                    query = """
                    INSERT INTO sf.coupons 
                    (coupon_uid, coupon_id, valid, discount_percent, discount_amount, discount_shipping, expire_date, limits, notes, num_used, recurring, email_id, cup_business_uid, threshold) 
                    VALUES ( \'""" + couponID + """\', \'""" + couponID + """\', \'""" + data['valid'] + """\', \'""" + data['discount_percent'] + """\', \'""" + data['discount_amount'] + """\', \'""" + data['discount_shipping'] + """\', \'""" + data['expire_date'] + """\', \'""" + data['limits'] + """\', \'""" + data['notes'] + """\', \'""" + '0' + """\', \'""" + data['recurring'] + """\', \'""" + data['email_id'] + """\', \'""" + data['cup_business_uid'] + """\', \'""" + data['threshold'] + """\');
                    """
                    print(query)
                    items = execute(query, 'post', conn)
                    if items['code'] != 281:
                        items['message'] = "check sql query"
                        items['code'] = 400
                        return items


                    items['message'] = 'Coupon info created'
                    items['code'] = 200
                    return items

                elif action == 'update':
                    print(data)
                    query = """
                    SELECT *
                    FROM sf.coupons
                    WHERE coupon_uid = \'""" + data['coupon_uid'] + """\';
                    """

                    items = execute(query, 'get', conn)
                    if not items['result']:
                        items['message'] = "Coupon uid doesn't exists"
                        items['code'] = 404
                        return items

                    query = """
                    UPDATE sf.coupons 
                    SET 
                    coupon_id = \'""" + data['coupon_uid'] + """\', 
                    valid = \'""" + data['valid'] + """\', 
                    discount_percent = \'""" + data['discount_percent'] + """\', 
                    discount_amount = \'""" + data['discount_amount'] + """\', 
                    discount_shipping = \'""" + data['discount_shipping'] + """\', 
                    expire_date = \'""" + data['expire_date'] + """\', 
                    limits = \'""" + data['limits'] + """\', 
                    notes = \'""" + data['notes'] + """\', 
                    num_used = \'""" + data['num_used'] + """\', 
                    recurring = \'""" + data['recurring'] + """\', 
                    email_id = \'""" + data['email_id'] + """\',
                    threshold = \'""" + data['threshold'] + """\', 
                    cup_business_uid = \'""" + data['cup_business_uid'] + """\' 
                    WHERE (coupon_uid = \'""" + data['coupon_uid'] + """\');
                    """

                    items = execute(query, 'post', conn)
                    print(items)
                    if items['code'] != 281:
                        items['message'] = "check sql query"
                        items['code'] = 400
                        return items

                    items['message'] = 'Coupon info updated'
                    items['code'] = 200
                    return items

                elif action == 'subtract':

                    query = """
                    SELECT *
                    FROM sf.coupons
                    WHERE coupon_uid = \'""" + data['coupon_uid'] + """\';
                    """

                    items = execute(query, 'get', conn)
                    if not items['result']:
                        items['message'] = "Coupon uid doesn't exists"
                        items['code'] = 404
                        return items

                    query = """
                            UPDATE sf.coupons SET num_used = num_used - 1 WHERE (coupon_uid = \'""" + data['coupon_uid'] + """\');
                            """
                    items = execute(query, 'post', conn)
                    items['message'] = 'Coupon info updated'
                    items['code'] = 200
                    return items


                elif action == 'add':

                    query = """
                    SELECT *
                    FROM sf.coupons
                    WHERE coupon_uid = \'""" + data['coupon_uid'] + """\';
                    """

                    items = execute(query, 'get', conn)
                    if not items['result']:
                        items['message'] = "Coupon uid doesn't exists"
                        items['code'] = 404
                        return items

                    query = """
                            UPDATE sf.coupons SET num_used = num_used + 1 WHERE (coupon_uid = \'""" + data['coupon_uid'] + """\');
                            """
                    items = execute(query, 'post', conn)
                    items['message'] = 'Coupon info updated'
                    items['code'] = 200
                    return items



                else:

                    items['message'] = 'Choose correct option'
                    items['code'] = 500
                    return items


            except:
                print("Error happened while updating coupon table")
                raise BadRequest('Request failed, please try again later.')
            finally:
                disconnect(conn)
                print('process completed')







# -- Farmers Queries End here -------------------------------------------------------------------------------


# -- Admin Queries Start here -------------------------------------------------------------------------------



#-- Analytics
class admin_report(Resource):

    def get(self, uid):

        try:
            conn = connect()

            query = """
                    SELECT *,deconstruct.*, sum(price) as Amount  
                    FROM sf.purchases, 
                         JSON_TABLE(items, '$[*]' COLUMNS (
                                    qty VARCHAR(255)  PATH '$.qty',
                                    name VARCHAR(255)  PATH '$.name',
                                    price VARCHAR(255)  PATH '$.price',
                                    item_uid VARCHAR(255)  PATH '$.item_uid',
                                    itm_business_uid VARCHAR(255) PATH '$.itm_business_uid')
                         ) AS deconstruct
                    WHERE itm_business_uid = \'""" + uid + """\'
                    GROUP BY purchase_uid;
                    """

            items = execute(query, 'get', conn)
            if items['code'] == 280:
                items['message'] = 'Report data successful'
                items['code'] = 200
            else:
                items['message'] = 'Check sql query'
            return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)


class summary_reports(Resource):

    def get(self, category,start,end):

        try:
            conn = connect()
            if category == 'business':
                query = """
                        SELECT itms_business_uid, sum(revenue_business) AS Revenue_business, sum(revenue_item) AS Revenue_item, sum(revenue_item) - sum(revenue_business) AS Profit, count(DISTINCT purchase_uid) AS Orders, count(DISTINCT pur_customer_uid) AS Customers, business_name
                        FROM
                        (SELECT *, (itm.business_price * qty) AS revenue_business, (itm.item_price * qty) AS revenue_item
                        FROM sf.purchases AS pur, sf.payments AS pay, sf.items AS itm, sf.businesses AS bus, 
                             JSON_TABLE(items, '$[*]' COLUMNS (
                                        qty VARCHAR(255)  PATH '$.qty',
                                        name VARCHAR(255)  PATH '$.name',
                                        price VARCHAR(255)  PATH '$.price',
                                        items_uid VARCHAR(255)  PATH '$.item_uid',
                                        itms_business_uid VARCHAR(255) PATH '$.itm_business_uid')
                             ) AS deconstruct
                        WHERE pur.purchase_uid = pay.pay_purchase_uid 
                              AND deconstruct.items_uid = itm.item_uid 
                              AND purchase_status = 'ACTIVE'
                              AND deconstruct.itms_business_uid = bus.business_uid
                              AND start_delivery_date BETWEEN \'""" + start + ' 00:00:00'  """\'  AND '""" + end + ' 23:59:59'  """\') AS res
                        GROUP BY itms_business_uid;
                        """

                items = execute(query, 'get', conn)
                if items['code'] == 280:
                    items['message'] = 'Report data successful'
                    items['code'] = 200
                else:
                    items['message'] = 'Check sql query'
                return items
            elif category == 'customer':
                query = """
                        SELECT sum(revenue_business) AS Revenue_business, sum(revenue_item) AS Revenue_item, sum(revenue_item) - sum(revenue_business) AS Profit, count(DISTINCT purchase_uid) AS Orders, delivery_first_name, delivery_last_name, pur_customer_uid
                        FROM
                        (SELECT *, (itm.business_price * qty) AS revenue_business, (itm.item_price * qty) AS revenue_item
                        FROM sf.purchases AS pur, sf.payments AS pay, sf.items AS itm,
                             JSON_TABLE(items, '$[*]' COLUMNS (
                                        qty VARCHAR(255)  PATH '$.qty',
                                        name VARCHAR(255)  PATH '$.name',
                                        price VARCHAR(255)  PATH '$.price',
                                        items_uid VARCHAR(255)  PATH '$.item_uid',
                                        itms_business_uid VARCHAR(255) PATH '$.itm_business_uid')
                             ) AS deconstruct
                        WHERE pur.purchase_uid = pay.pay_purchase_uid 
                              AND deconstruct.items_uid = itm.item_uid
                              AND purchase_status = 'ACTIVE'
                              AND start_delivery_date BETWEEN \'""" + start + ' 00:00:00'  """\'  AND '""" + end + ' 23:59:59'  """\') AS res
                        GROUP BY pur_customer_uid;
                        """

                items = execute(query, 'get', conn)
                if items['code'] == 280:
                    items['message'] = 'Report data successful'
                    items['code'] = 200
                else:
                    items['message'] = 'Check sql query'
                return items
            elif category == 'item':
                query = """
                        SELECT sum(revenue_business) AS Revenue_business, sum(revenue_item) AS Revenue_item, sum(revenue_item) - sum(revenue_business) AS Profit, sum(qty) AS Orders, count(DISTINCT pur_customer_uid) AS Customer, name
                        FROM
                        (SELECT *, (itm.business_price * qty) AS revenue_business, (itm.item_price * qty) AS revenue_item
                        FROM sf.purchases AS pur, sf.payments AS pay, sf.items AS itm, 
                             JSON_TABLE(items, '$[*]' COLUMNS (
                                        qty VARCHAR(255)  PATH '$.qty',
                                        name VARCHAR(255)  PATH '$.name',
                                        price VARCHAR(255)  PATH '$.price',
                                        items_uid VARCHAR(255)  PATH '$.item_uid',
                                        itms_business_uid VARCHAR(255) PATH '$.itm_business_uid')
                             ) AS deconstruct
                        WHERE pur.purchase_uid = pay.pay_purchase_uid 
                              AND deconstruct.items_uid = itm.item_uid
                              AND purchase_status = 'ACTIVE'
                              AND start_delivery_date BETWEEN \'""" + start + ' 00:00:00'  """\'  AND '""" + end + ' 23:59:59'  """\') AS res
                        GROUP BY items_uid;
                        """

                items = execute(query, 'get', conn)
                if items['code'] == 280:
                    items['message'] = 'Report data successful'
                    items['code'] = 200
                else:
                    items['message'] = 'Check sql query'
                return items
            else:
                return 'choose correct category'

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)




#-- End Analytics

class report_order_customer_pivot_detail(Resource):

    def get(self, report, uid):

        try:
            conn = connect()
            if report == 'order':
                query = """
                        SELECT purchase_uid, purchase_date, delivery_first_name, delivery_last_name, delivery_phone_num, delivery_email, delivery_address, delivery_unit, delivery_city, delivery_state, delivery_zip, deconstruct.*, amount_paid, (SELECT business_name from sf.businesses WHERE business_uid = itm_business_uid) AS business_name
                        FROM sf.purchases, sf.payments,
                             JSON_TABLE(items, '$[*]' COLUMNS (
                                        qty VARCHAR(255)  PATH '$.qty',
                                        name VARCHAR(255)  PATH '$.name',
                                        price VARCHAR(255)  PATH '$.price',
                                        item_uid VARCHAR(255)  PATH '$.item_uid',
                                        itm_business_uid VARCHAR(255) PATH '$.itm_business_uid')
                             ) AS deconstruct
                        WHERE purchase_uid = pay_purchase_uid AND purchase_status = 'ACTIVE' AND itm_business_uid = \'""" + uid + """\';
                        """

                items = execute(query, 'get', conn)

                if items['code'] != 280:
                    items['message'] = 'Check sql query'
                    return items
                else:

                    items['message'] = 'Report data successful'
                    items['code'] = 200
                    result = items['result']
                    dict = {}
                    for vals in result:
                        if vals['purchase_uid'] in dict:
                            dict[vals['purchase_uid']].append(vals)
                        else:
                            dict[vals['purchase_uid']] = [vals]

                    data = []

                    for key, vals in dict.items():

                        tmp = vals[0]
                        print('tmp----', tmp)
                        data.append([tmp['purchase_date'],
                                     tmp['delivery_first_name'],
                                     tmp['delivery_last_name'],
                                     tmp['delivery_phone_num'],
                                     tmp['delivery_email'],
                                     tmp['delivery_address'],
                                     tmp['delivery_unit'],
                                     tmp['delivery_city'],
                                     tmp['delivery_state'],
                                     tmp['delivery_zip'],
                                     tmp['amount_paid']
                                     ])
                        for items in vals:
                            data.append([items['name'],
                                        items['qty'],
                                        items['price']
                                        ])


                    si = io.StringIO()
                    cw = csv.writer(si)
                    cw.writerow(['Open Orders'])
                    for item in data:
                        cw.writerow(item)

                    orders = si.getvalue()
                    output = make_response(orders)
                    output.headers["Content-Disposition"] = "attachment; filename=order_details.csv"
                    output.headers["Content-type"] = "text/csv"
                    return output
            elif report == 'customer':
                query = """
                        SELECT pur_customer_uid, purchase_uid, purchase_date, delivery_first_name, delivery_last_name, delivery_phone_num, delivery_email, delivery_address, delivery_unit, delivery_city, delivery_state, delivery_zip, deconstruct.*, amount_paid, sum(price) as Amount
                        FROM sf.purchases, sf.payments,
                             JSON_TABLE(items, '$[*]' COLUMNS (
                                        qty VARCHAR(255)  PATH '$.qty',
                                        name VARCHAR(255)  PATH '$.name',
                                        price VARCHAR(255)  PATH '$.price',
                                        item_uid VARCHAR(255)  PATH '$.item_uid',
                                        itm_business_uid VARCHAR(255) PATH '$.itm_business_uid')
                             ) AS deconstruct
                        WHERE purchase_uid = pay_purchase_uid AND purchase_status = 'ACTIVE' AND itm_business_uid = \'""" + uid + """\'
                        GROUP BY pur_customer_uid;
                        """

                items = execute(query, 'get', conn)

                if items['code'] != 280:
                    items['message'] = 'Check sql query'
                    return items
                else:

                    items['message'] = 'Report data successful'
                    items['code'] = 200
                    result = items['result']
                    print('result------', result)
                    data = []

                    for vals in result:

                        tmp = vals
                        print('tmp----', tmp)
                        data.append([tmp['delivery_first_name'],
                                     tmp['delivery_last_name'],
                                     tmp['delivery_phone_num'],
                                     tmp['delivery_email'],
                                     tmp['delivery_address'],
                                     tmp['delivery_unit'],
                                     tmp['delivery_city'],
                                     tmp['delivery_state'],
                                     tmp['delivery_zip'],
                                     tmp['Amount']
                                     ])

                    si = io.StringIO()
                    cw = csv.writer(si)
                    for item in data:
                        cw.writerow(item)

                    orders = si.getvalue()
                    output = make_response(orders)
                    output.headers["Content-Disposition"] = "attachment; filename=customer_details.csv"
                    output.headers["Content-type"] = "text/csv"
                    return output
            elif report == 'pivot':
                query = """
                        SELECT pur_customer_uid, purchase_uid, purchase_date, delivery_first_name, delivery_last_name, delivery_phone_num, delivery_email, delivery_address, delivery_unit, delivery_city, delivery_state, delivery_zip, deconstruct.*, amount_paid, (SELECT business_name from sf.businesses WHERE business_uid = itm_business_uid) AS business_name
                        FROM sf.purchases, sf.payments,
                             JSON_TABLE(items, '$[*]' COLUMNS (
                                        qty VARCHAR(255)  PATH '$.qty',
                                        name VARCHAR(255)  PATH '$.name',
                                        price VARCHAR(255)  PATH '$.price',
                                        item_uid VARCHAR(255)  PATH '$.item_uid',
                                        itm_business_uid VARCHAR(255) PATH '$.itm_business_uid')
                             ) AS deconstruct
                        WHERE purchase_uid = pay_purchase_uid AND purchase_status = 'ACTIVE' AND itm_business_uid = \'""" + uid + """\';
                        """

                items = execute(query, 'get', conn)

                if items['code'] != 280:
                    items['message'] = 'Check sql query'
                    return items
                else:

                    items['message'] = 'Report data successful'
                    items['code'] = 200
                    result = items['result']
                    itm_dict = {}
                    for vals in result:
                        if vals['name'] in itm_dict:
                            itm_dict[vals['name']] += int(vals['qty'])
                        else:
                            itm_dict[vals['name']] = int(vals['qty'])
                    print('ddddddd------', itm_dict)
                    dict = {}
                    for vals in result:
                        if vals['pur_customer_uid'] in dict:
                            dict[vals['pur_customer_uid']].append(vals)
                        else:
                            dict[vals['pur_customer_uid']] = [vals]

                    print('dict----', dict)
                    si = io.StringIO()
                    cw = csv.DictWriter(si, ['Name', 'Email', 'Phone', 'Total'] + list(itm_dict.keys()))
                    cw.writeheader()
                    glob_tot = 0
                    for key, vals in dict.items():
                        print('VALSSS---', vals)
                        items = {groc['name']:groc['qty'] for groc in vals}
                        total_sum = 0
                        for tp_key, tp_vals in items.items():
                            total_sum += int(tp_vals)
                        glob_tot += total_sum
                        print('items-----------------', items)
                        items['Name'] = vals[0]['delivery_first_name'] + vals[0]['delivery_last_name']
                        items['Email'] = vals[0]['delivery_email']
                        items['Phone'] = vals[0]['delivery_phone_num']
                        items['Total'] = total_sum
                        cw.writerow(items)

                    cw.writerow({'Name': 'Total', 'Total': glob_tot, **itm_dict})

                    orders = si.getvalue()
                    output = make_response(orders)
                    output.headers["Content-Disposition"] = "attachment; filename=pivot_table.csv"
                    output.headers["Content-type"] = "text/csv"
                    return output
            else:
                return "choose correct option"
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)

class farmer_revenue_inventory_report(Resource):

    def post(self, report):

        try:
            conn = connect()
            data = request.get_json(force=True)
            query = """
                    SELECT business_name FROM sf.businesses
                    WHERE business_uid = \'""" + data['uid'] + """\';
                    """
            items = execute(query, 'get', conn)
            if items['code'] != 280:
                items['message'] = "Business UID doesn't exsist"
                return items
            print(items)
            business_name = items['result'][0]['business_name']
            query = """
                    SELECT obf.*, pay.start_delivery_date, pay.payment_uid, itm.business_price, SUM(obf.qty) AS total_qty, SUM(itm.business_price) AS total_price, itm.item_unit
                    FROM sf.orders_by_farm AS obf, sf.payments AS pay, sf.items AS itm
                    WHERE obf.purchase_uid = pay.pay_purchase_uid AND obf.item_uid = itm.item_uid AND pay.start_delivery_date LIKE \'""" + data['delivery_date'] + '%' + """\' AND obf.itm_business_uid = \'""" + data['uid'] + """\'
                    GROUP BY  obf.delivery_address, obf.delivery_unit, obf.delivery_city, obf.delivery_state, obf.delivery_zip, obf.item_uid;
                    """
            print(query)
            items = execute(query, 'get', conn)
            if items['code'] != 280:
                items['message'] = 'Check sql query'
                return items

            result = items['result']
            itm_dict = {}
            cust_dict = {}
            for vals in result:
                if vals['name'] in itm_dict:
                    itm_dict[vals['name']][0] += int(vals['total_qty'])
                else:
                    itm_dict[vals['name']] = [int(vals['total_qty']), vals['business_price'], vals['item_unit']]
            print('dict------', itm_dict)

            for vals in result:
                unq = (vals['delivery_address'], vals['delivery_unit'], vals['delivery_city'], vals['delivery_state'], vals['delivery_zip'])
                print(unq)
                if unq in itm_dict:
                    cust_dict[unq][0] += int(vals['total_qty'])
                else:
                    cust_dict[unq] = [int(vals['total_qty']), vals['business_price'], vals['item_unit']]

            print('cust_dict------', cust_dict)
            si = io.StringIO()
            cw = csv.writer(si)
            cw.writerow([business_name])
            cw.writerow([])
            cw.writerow([])
            itm_dict = dict(sorted(itm_dict.items(), key=lambda x: x[0].lower()))

            if report == 'summary':
                glob_rev = 0
                cw.writerow(['Item', 'Quantity', 'Revenue'])
                for key, vals in itm_dict.items():
                    print(key)
                    itm_rev = 0
                    itm_qty = 0
                    rr = []
                    for vals in result:
                        if vals['name'] == key:
                            itm_qty += vals['total_qty']
                            itm_rev += vals['total_qty']*vals['business_price']
                    cw.writerow([key, itm_qty, itm_rev])
                    glob_rev += itm_rev

                cw.writerow(['TOTAL REVENUE', glob_rev])
                orders = si.getvalue()

                ###

                query = """
                        SELECT business_email from sf.businesses WHERE business_uid = \'""" + data['uid'] + """\';
                        """

                items = execute(query, 'get', conn)
                if items['code'] != 280:
                    items['message'] = 'business email query failed'
                    return items
                email = items['result'][0]['business_email']
                print(email)

                msg = Message(business_name + " Summary Report for " + data['delivery_date'], sender='support@servingfresh.me', recipients=[email])

                #msg.body = "Click on the link {} to verify your email address.".format(link)

                msg.body = "Hi " + business_name + "!\n\n" \
                           "We are excited to send you your Summary report for delivery date " + data['delivery_date'] + \
                           ". Please find the report in the attachment. \n"\
                           "Email support@servingfresh.me if you run into any problems or have any questions.\n" \
                           "Thx - The Serving Fresh Team\n\n"
                msg.attach('Produce Summary Report - ' + data['delivery_date'] + '.csv', 'text/csv', orders)
                print('msg-bd----', msg.body)
                print('msg-')
                mail.send(msg)

                ###
                output = make_response(orders)
                output.headers["Content-Disposition"] = "attachment; filename=Produce Summary Report - " + data['delivery_date'] + ".csv"
                output.headers["Content-type"] = "text/csv"
                return output

            elif report == 'packing':

                for key, vals in itm_dict.items():
                    print(key)
                    rr = []
                    for vals in result:
                        if vals['name'] == key:
                            rr.append(int(vals['total_qty']))
                    rr.sort()
                    rr.insert(0, key)
                    cw.writerow(rr)

                query = """
                        SELECT business_email from sf.businesses WHERE business_uid = \'""" + data['uid'] + """\';
                        """

                items = execute(query, 'get', conn)
                if items['code'] != 280:
                    items['message'] = 'business email query failed'
                    return items
                email = items['result'][0]['business_email']
                print(email)

                orders = si.getvalue()

                ###
                msg = Message(business_name + " Packing Report for " + data['delivery_date'], sender='support@servingfresh.me', recipients=[email])

                #msg.body = "Click on the link {} to verify your email address.".format(link)

                msg.body = "Hi " + business_name + "!\n\n" \
                           "We are excited to send you your packaging report for delivery date " + data['delivery_date'] + \
                           ". Please find the report in the attachment. \n"\
                           "Email support@servingfresh.me if you run into any problems or have any questions.\n" \
                           "Thx - The Serving Fresh Team\n\n"
                msg.attach('Produce Packing Report - ' + data['delivery_date'] + '.csv', 'text/csv', orders)
                print('msg-bd----', msg.body)
                print('msg-')
                mail.send(msg)

                ###
                output = make_response(orders)
                output.headers["Content-Disposition"] = "attachment; filename=Produce Packing Report - " + data['delivery_date'] + ".csv"
                output.headers["Content-type"] = "text/csv"
                return output
            elif report == 'customer':

                for key, vals in cust_dict.items():
                    rr = []


            else:
                return 'choose correct report'

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)





# -- Admin Queries End here -------------------------------------------------------------------------------


# -- Queries end here -------------------------------------------------------------------------------







# -- NOTIFICATIONS Queries Start here -------------------------------------------------------------------------------

class customer_info(Resource):

    def get(self):

        try:
            conn = connect()
            query = """
                    SELECT 

                        custom.customer_uid,
                        custom.customer_first_name,
                        custom.customer_last_name,
                        custom.customer_email,
                        custom.customer_phone_num,
                        custom.customer_address,
                        custom.customer_unit,
                        custom.customer_city,
                        custom.customer_zip,
                        custom.cust_notification_approval,
                        custom.SMS_freq_preference,
                        custom.SMS_last_notification,
                        custom.cust_guid_device_id_notification,
                        DS.business_name,
                        DS.price,
                        DS.itm_business_uid,
                        DS.number_of_orders,
                        DS.latest_order_date
                    
                    FROM
                    (SELECT  
                    cust.customer_uid AS c_uid,
                    cust.customer_first_name,
                    cust.customer_last_name,
                    cust.customer_email,
                    cust.customer_phone_num,
                    cust.customer_address,
                    cust.customer_unit,
                    cust.customer_city,
                    cust.customer_zip,
                    cust.customer_created_at,
                    cust.cust_notification_approval,
                    cust.SMS_freq_preference,
                    cust.SMS_last_notification,
                    cust.cust_guid_device_id_notification,
                    pay.pay_purchase_uid,
                    (SELECT business_name FROM sf.businesses AS bus WHERE bus.business_uid = deconstruct.itm_business_uid) AS business_name,
                    deconstruct.*,
                    count(DISTINCT pay_purchase_uid) AS number_of_orders, 
                    max(pay.payment_time_stamp) AS latest_order_date
                                FROM sf.purchases , 
                                     JSON_TABLE(items, '$[*]' COLUMNS (
                                                qty VARCHAR(255)  PATH '$.qty',
                                                name VARCHAR(255)  PATH '$.name',
                                                price VARCHAR(255)  PATH '$.price',
                                                item_uid VARCHAR(255)  PATH '$.item_uid',
                                                itm_business_uid VARCHAR(255) PATH '$.itm_business_uid')
                                     ) AS deconstruct, sf.payments AS pay, sf.customers AS cust
                    WHERE purchase_uid = pay.pay_purchase_uid AND pur_customer_uid = cust.customer_uid
                    GROUP BY deconstruct.itm_business_uid, pur_customer_uid) AS DS
					RIGHT JOIN sf.customers AS custom
                    ON DS.c_uid = custom.customer_uid 
                    WHERE custom.cust_guid_device_id_notification <> CAST('null' AS JSON)
                    ;
                    """
            items = execute(query, 'get', conn)

            if items['code'] == 280:

                items['message'] = 'Customer info Loaded successful'
                items['code'] = 200
                return items
            else:
                items['message'] = "check sql query"
                items['code'] = 404
                return items

        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)



class Send_Twilio_SMS(Resource):

    def post(self):
        items = {}
        data = request.get_json(force=True)
        numbers = data['numbers']
        message = data['message']
        if not numbers:
            raise BadRequest('Request failed. Please provide the recipients field.')
        if not message:
            raise BadRequest('Request failed. Please provide the message field.')
        print('IN SMS----')
        print(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        for destination in numbers.split(','):
            client.messages.create(
                body = message,
                from_= '+19254815757',
                to = "+1" + destination
            )
        items['code'] = 200
        items['Message'] = 'SMS sent successfully to all recipients'
        return items







class Send_Notification(Resource):

    def post(self, role):

        def deconstruct(uids, role):

            conn = connect()
            uids_array = uids.split(',')
            output = []
            for uid in uids_array:
                if role == 'customer':
                    query = """SELECT cust_guid_device_id_notification FROM sf.customers WHERE customer_uid = \'""" + uid + """\';"""
                    items = execute(query, 'get', conn)

                    if items['code'] != 280:
                        items['message'] = "check sql query"
                        items['code'] = 404
                        return items

                    json_val = items['result'][0]['cust_guid_device_id_notification']

                else:

                    query = """SELECT bus_guid_device_id_notification FROM sf.businesses WHERE business_uid = \'""" + uid + """\';"""
                    items = execute(query, 'get', conn)

                    if items['code'] != 280:
                        items['message'] = "check sql query"
                        items['code'] = 404
                        return items

                    json_val = items['result'][0]['bus_guid_device_id_notification']

                if json_val != 'null':
                    print(type(json_val))
                    print(json_val)
                    input_val = json.loads(json_val)
                    print(type(input_val))
                    print(input_val)
                    for vals in input_val:
                        print('vals--', vals)
                        print(type(vals))
                        if vals == None:
                            continue
                        print('guid--', vals['guid'])
                        print('notification---', vals['notification'])
                        if vals['notification'] == 'TRUE':
                            output.append('guid_' + vals['guid'])
            output = ",".join(output)
            print('output-----', output)
            return output
        print('IN---')
        hub = NotificationHub(NOTIFICATION_HUB_KEY, NOTIFICATION_HUB_NAME, isDebug)
        print(hub)
        print('role----', role)
        uids = request.form.get('uids')
        message = request.form.get('message')
        print('uids', uids)
        print('role', role)
        tags = deconstruct(uids, role)
        print('tags-----', tags)
        if tags == []:
            return 'No GUIDs found for the UIDs provided'
        #tags = uids
        if tags is None:
            raise BadRequest('Request failed. Please provide the tag field.')
        if message is None:
            raise BadRequest('Request failed. Please provide the message field.')
        tags = tags.split(',')
        for tag in tags:
            print('tag-----', tag)
            print(type(tag))
            alert_payload = {
                "aps" : {
                    "alert" : message,
                },
            }
            hub.send_apple_notification(alert_payload, tags = tag)

            fcm_payload = {
                "data":{"message": message}
            }
            hub.send_gcm_notification(fcm_payload, tags = tag)

        return 200


class Get_Registrations_From_Tag(Resource):
    def get(self, tag):
        hub = NotificationHub(NOTIFICATION_HUB_KEY, NOTIFICATION_HUB_NAME, isDebug)
        if tag is None:
            raise BadRequest('Request failed. Please provide the tag field.')
        response = hub.get_all_registrations_with_a_tag(tag)
        response = str(response.read())
        print(response)
        return response,200

class Create_or_Update_Registration_iOS(Resource):
    def post(self):
        hub = NotificationHub(NOTIFICATION_HUB_KEY, NOTIFICATION_HUB_NAME, isDebug)
        registration_id = request.form.get('registration_id')
        device_token = request.form.get('device_token')
        tags = request.form.get('tags')

        if tags is None:
            raise BadRequest('Request failed. Please provide the tags field.')
        if registration_id is None:
            raise BadRequest('Request failed. Please provide the registration_id field.')
        if device_token is None:
            raise BadRequest('Request failed. Please provide the device_token field.')

        response = hub.create_or_update_registration_iOS(registration_id, device_token, tags)

        return response.status

class Update_Registration_With_GUID_iOS(Resource):
    def post(self):
        hub = NotificationHub(NOTIFICATION_HUB_KEY, NOTIFICATION_HUB_NAME, isDebug)
        guid = request.form.get('guid')
        tags = request.form.get('tags')
        if guid is None:
            raise BadRequest('Request failed. Please provide the guid field.')
        if tags is None:
            raise BadRequest('Request failed. Please provide the tags field.')
        response = hub.get_all_registrations_with_a_tag(guid)
        xml_response = str(response.read())[2:-1]
        # root = ET.fromstring(xml_response)
        xml_response_soup = BeautifulSoup(xml_response,features="html.parser")
        appleregistrationdescription = xml_response_soup.feed.entry.content.appleregistrationdescription
        registration_id = appleregistrationdescription.registrationid.get_text()
        device_token = appleregistrationdescription.devicetoken.get_text()
        old_tags = appleregistrationdescription.tags.get_text().split(",")
        tags = tags.split(",")
        new_tags = set(old_tags + tags)
        new_tags = ','.join(new_tags)
        print(f"tags: {old_tags}\ndevice_token: {device_token}\nregistration_id: {registration_id}")

        if device_token is None or registration_id is None:
            raise BadRequest('Something went wrong in retriving device_token and registration_id')

        response = hub.create_or_update_registration_iOS(registration_id, device_token, new_tags)
        # for type_tag in root.findall('feed/entry/content/AppleRegistrationDescription'):
        #     value = type_tag.get('Tags')
        #     print(value)
        # print("\n\n--- RESPONSE ---")
        # print(str(response.status) + " " + response.reason)
        # print(response.msg)
        # print(response.read())
        # print("--- END RESPONSE ---")
        return response.status

class Update_Registration_With_GUID_Android(Resource):
    def post(self):
        hub = NotificationHub(NOTIFICATION_HUB_KEY, NOTIFICATION_HUB_NAME, isDebug)
        guid = request.form.get('guid')
        tags = request.form.get('tags')
        if guid is None:
            raise BadRequest('Request failed. Please provide the guid field.')
        if tags is None:
            raise BadRequest('Request failed. Please provide the tags field.')
        response = hub.get_all_registrations_with_a_tag(guid)
        xml_response = str(response.read())[2:-1]
        # root = ET.fromstring(xml_response)
        xml_response_soup = BeautifulSoup(xml_response,features="html.parser")
        gcmregistrationdescription = xml_response_soup.feed.entry.content.gcmregistrationdescription
        registration_id = gcmregistrationdescription.registrationid.get_text()
        gcm_registration_id = gcmregistrationdescription.gcmregistrationid.get_text()
        old_tags = gcmregistrationdescription.tags.get_text().split(",")
        tags = tags.split(",")
        new_tags = set(old_tags + tags)
        new_tags = ','.join(new_tags)
        print(f"tags: {old_tags}\nregistration_id: {registration_id}\ngcm_registration_id: {gcm_registration_id}")

        if gcm_registration_id is None or registration_id is None:
            raise BadRequest('Something went wrong in retriving gcm_registration_id and registration_id')

        response = hub.create_or_update_registration_android(registration_id, gcm_registration_id, new_tags)
        return response.status

class Get_Tags_With_GUID_iOS(Resource):
    def get(self, tag):
        hub = NotificationHub(NOTIFICATION_HUB_KEY, NOTIFICATION_HUB_NAME, isDebug)
        guid = tag
        if guid is None:
            raise BadRequest('Request failed. Please provide the guid field.')
        response = hub.get_all_registrations_with_a_tag(guid)
        print(response)
        xml_response = str(response.read())[2:-1]
        # root = ET.fromstring(xml_response)
        xml_response_soup = BeautifulSoup(xml_response,features="html.parser")
        appleregistrationdescription = xml_response_soup.feed.entry.content.appleregistrationdescription
        registration_id = appleregistrationdescription.registrationid.get_text()
        device_token = appleregistrationdescription.devicetoken.get_text()
        old_tags = appleregistrationdescription.tags.get_text().split(",")
        return old_tags

# -- NOTIFICATIONS Queries End here -------------------------------------------------------------------------------


# Define API routes

api.add_resource(Businesses, '/api/v2/businesses')
api.add_resource(ItemsbyBusiness, '/api/v2/itemsByBusiness/<string:business_uid>')
api.add_resource(SubscriptionsbyBusiness, '/api/v2/subscriptionsByBusiness/<string:business_uid>')
api.add_resource(CouponDetails, '/api/v2/couponDetails/<string:coupon_id>', '/api/v2/couponDetails')
api.add_resource(RefundDetails, '/api/v2/refundDetails')
api.add_resource(PurchaseData, '/api/v2/purchaseData')
api.add_resource(MSPurchaseData, '/api/v2/MSpurchaseData')

# Customer Endpoints

api.add_resource(token_fetch_update, '/api/v2/token_fetch_update/<string:action>')
#api.add_resource(SignUp, '/api/v2/SignUp') -- Note : for some reason does not work on SF xamarin code
api.add_resource(createAccount, '/api/v2/createAccount')
api.add_resource(email_verification, '/api/v2/email_verification')
api.add_resource(AccountSalt, '/api/v2/AccountSalt')
api.add_resource(Login, '/api/v2/Login/')
api.add_resource(AppleLogin, '/api/v2/AppleLogin', '/')
api.add_resource(access_refresh_update, '/api/v2/access_refresh_update')
api.add_resource(Profile, '/api/v2/Profile/<string:id>')
api.add_resource(update_Profile, '/api/v2/update_Profile')
api.add_resource(update_email_password, '/api/v2/update_email_password')
api.add_resource(update_guid_notification, '/api/v2/update_guid_notification/<string:role>,<string:action>')
api.add_resource(Refund, '/api/v2/Refund')
api.add_resource(categoricalOptions, '/api/v2/categoricalOptions/<string:long>,<string:lat>')
api.add_resource(getItems, '/api/v2/getItems')
api.add_resource(purchase, '/api/v2/purchase')
api.add_resource(payment, '/api/v2/payment')
api.add_resource(available_Coupons, '/api/v2/available_Coupons/<string:email>')
api.add_resource(history, '/api/v2/history/<string:uid>')
api.add_resource(get_Fee_Tax, '/api/v2/get_Fee_Tax/<string:z_id>,<string:day>')
api.add_resource(purchase_Data_SF, '/api/v2/purchase_Data_SF')
api.add_resource(Stripe_Intent, '/api/v2/Stripe_Intent')
api.add_resource(Stripe_Payment_key_checker, '/api/v2/Stripe_Payment_key_checker')
api.add_resource(Paypal_Payment_key_checker, '/api/v2/Paypal_Payment_key_checker')


# Farmer Endpoints

api.add_resource(addItems, '/api/v2/addItems/<string:action>')
api.add_resource(all_businesses, '/api/v2/all_businesses')
api.add_resource(business_details_update, '/api/v2/business_details_update/<string:action>')
api.add_resource(orders_by_farm, '/api/v2/orders_by_farm')
api.add_resource(orders_info, '/api/v2/orders_info')
api.add_resource(orderSummary, '/api/v2/orderSummary')
api.add_resource(order_actions, '/api/v2/order_actions/<string:action>')
api.add_resource(update_all_items, '/api/v2/update_all_items/<string:uid>')
api.add_resource(get_item_photos, '/api/v2/get_item_photos/<string:category>')
api.add_resource(update_Coupons, '/api/v2/update_Coupons/<string:action>')

# Admin Endpoints

api.add_resource(admin_report, '/api/v2/admin_report/<string:uid>')
api.add_resource(summary_reports, '/api/v2/summary_reports/<string:category>,<string:start>,<string:end>')
api.add_resource(report_order_customer_pivot_detail, '/api/v2/report_order_customer_pivot_detail/<string:report>,<string:uid>')
api.add_resource(farmer_revenue_inventory_report, '/api/v2/farmer_revenue_inventory_report/<string:report>')

# Notification Endpoints

api.add_resource(customer_info, '/api/v2/customer_info')
api.add_resource(Send_Twilio_SMS, '/api/v2/Send_Twilio_SMS')
api.add_resource(Send_Notification, '/api/v2/Send_Notification/<string:role>')
api.add_resource(Get_Registrations_From_Tag, '/api/v2/Get_Registrations_From_Tag/<string:tag>')
api.add_resource(Update_Registration_With_GUID_iOS, '/api/v2/Update_Registration_With_GUID_iOS')
api.add_resource(Update_Registration_With_GUID_Android, '/api/v2/Update_Registration_With_GUID_Android')
api.add_resource(Get_Tags_With_GUID_iOS, '/api/v2/Get_Tags_With_GUID_iOS/<string:tag>')



#Create_or_Update_Registration_iOS
#Update_Registration_With_GUID_Android

# Run on below IP address and port
# Make sure port number is unused (i.e. don't use numbers 0-1023)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
    #app.run(host='0.0.0.0', port=2000)




