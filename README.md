# Information about all the endpoints

### SIGNUP

[Post]

endpoint:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/SignUp

input:

{"email" : "xyz@gmail.com",\
"first_name" : "xyz",\
"last_name" : "abc",\
"phone_number" : "9876549879",\
"address" : "955 W President",\
"unit" : "3452",\
"city" : "Dallas",\
"state" : "TX",\
"zip_code" : "75980",\
"latitude" : "-14.3",\
"longitude" : "94.3",\
"referral_source" : "WEB",\
"role" : "CUSTOMER",\
"access_token" : "NULL",\
"refresh_token": "NULL",\
"social" : "FALSE",\
"password": "work123",\
"cust_id": "100-000236" ----- optional [if you are using APPLE login then only use this variable else don't include it in json]
}

NOTE:

For customers using email and password above input is valid but if customer uses social signup do
update access_token, social = TRUE and refresh_token field respectively.

return:

{
"message": "Signup successful",\
"code": 200,\
"result": {\
        "first_name": "xyz",\
        "last_name": "abc",\
        "customer_uid": "100-000094",\
        "access_token": "NULL",\
        "refresh_token": "NULL"\
        }\
}



### AccountSalt

[Get]

endpoint:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/AccountSalt

input:\
{\
"email" : "xyz@gmail.com"\
}

return: password_algorithm and password_salt

NOTE:

Use this endpoint only if user logins with email and password


### Login

[Post]

endpoint: https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Login/

input:

Example 1:\
{\
"email" : "annrupp22@gmail.com",\
"password" : "4178980d28dcec5b36521c1a9beeef791db4e6674aa77",\
"token" : "",\
"signup_platform" : ""\
}

Example 2:\
{\
"email" : "llshen@scu.edu",\
"password" : "",\
"token" : "114258941436931104766",\
"signup_platform" : "GOOGLE"\
}

NOTE: \
Input to email is Mandatory\
Input to password will be empty string "" if social media signup is there.\
Input to token will be empty string "" if social media signup is NOT there.\
Input to signup_platform will be empty string "" if social media signup is NOT there else GOOGLE, FACEBOOK or APPLE.


return:

All the details of that customer

Error Codes:

500 - internal server error -- Try again\
404 - Email not found -- Redirect to signup page\
401 - Need to login by social media\
405 - Password not entered and no refresh token available in database -- Redirect to signup page\
406 - Wrong password\
407 - Account not verified\
408 - Token incorrect\
500 - Cannot compare the password or refresh token while log in. -- Try again\
200 - Successful login


### Profile

[Get]


endpoint: https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Profile/id

example:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Profile/100-000232

return: all the details about customer


### getItems

[Post]

endpoint:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/getItems

input:

{\
"type" : ["fruit","desert"],\
"ids" : ["200-000003","200-000004","200-000005"]\
}

return: information of all items available filtered by business ids and type of item.


### Categorical_Options

[Get]

endpoint:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Categorical_Options/longitude,latitude

example: https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Categorical_Options/-121.928472,37.24370


return: information of all businesses and type of food category available in that business within field item_type

{\
"business_uid": "200-000001",\
"business_created_at": "2020-01-09T17:34:48",\
"business_name": "PTYD",\
"business_type": "toomuch",\
"business_desc": "Vegan Delivery Service",\
"business_association": null,\
"business_contact_first_name": "Heather",\
"business_contact_last_name": "Faiez",\
"business_phone_num": "(512) 555-1234",\
"business_phone_num2": "(512) 555-1200",\
"business_email": "heather@ptyd.com",\
"business_hours": "{"Friday": ["00:00:00", "23:59:00"], "Monday": ["00:00:00", "23:59:00"], "Sunday": ["00:00:00", "23:59:00"], "Tuesday": ["00:00:00", "23:59:00"], "Saturday": ["00:00:00", "23:59:00"], "Thursday": ["00:00:00", "23:59:00"], "Wednesday": ["00:00:00", "23:59:00"]}",\
"business_accepting_hours": "{"Friday": ["09:00:00", "23:59:59"], "Monday": ["09:00:00", "23:59:59"], "Sunday": ["09:00:00", "23:59:59"], "Tuesday": ["09:00:00", "23:59:59"], "Saturday": ["09:00:00", "21:00:00"], "Thursday": ["09:00:00", "23:59:59"], "Wednesday": ["09:00:00", "23:00:00"]}",\
"business_delivery_hours": "{"Friday": ["09:00:00", "23:59:59"], "Monday": ["00:00:00", "00:00:00"], "Sunday": ["09:00:00", "23:59:59"], "Tuesday": ["09:00:00", "23:59:59"], "Saturday": ["09:00:00", "21:00:00"], "Thursday": ["09:00:00", "23:59:59"], "Wednesday": ["09:00:00", "23:00:00"]}",\
"business_address": "360 Cowden Road",\
"business_unit": "",\
"business_city": "Hollister",\
"business_state": "CA",\
"business_zip": "95135",\
"business_longitude": "-121.9141246",\
"business_latitude": "37.3316565",\
"business_EIN": "",\
"business_WAUBI": "",\
"business_license": "",\
"business_USDOT": "",\
"notification_approval": "",\
"notification_device_id": "",\
"can_cancel": 0,\
"delivery": 0,\
"reusable": 0,\
"business_image": "https://servingnow.s3-us-west-1.amazonaws.com/kitchen_imgs/landing-logo.png",\
"business_password": "pbkdf2:sha256:150000$zMHfn0jt$29cef351d84456b5f6b665bc2bbab8ae3c6e42bd0e4a4e8967041a9455a24798",\
"itm_business_uid": "200-000001",\
"item_type": "dessert,fruit,other,vegetable"\
}



### Refund

[Post]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Refund

input: {"image_url":"http://servingnow.me","email":"abc@gmail.com","note":"Please issue a refund for eggplant" }

return: code either 200 or 400. If 200 refund ticket generated else email doesn't exists


### available_Coupons

[Get]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/available_Coupons/email

example:    https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/available_Coupons/xyz@gmail.com

return: json object with all general available coupons and coupons associated with the specified email id

[{\
            "coupon_uid": "600-000001",\
            "coupon_id": "AlmadenMeadows",\
            "valid": "TRUE",\
            "discount_percent": 50,\
            "discount_amount": 0,\
            "discount_shipping": 0,\
            "expire_date": "2021-05-31",\
            "limits": 17,\
            "notes": "Free Delivey",\
            "num_used": 11,\
            "recurring": "T",\
            "email_id": "",\
            "cup_business_uid": ""\
        },\
        {\
            "coupon_uid": "600-000002",\
            "coupon_id": "ann1475",\
            "valid": "TRUE",\
            "discount_percent": 0,\
            "discount_amount": 0,\
            "discount_shipping": 0,\
            "expire_date": "2020-05-22",\
            "limits": 2,\
            "notes": "Lost Order",\
            "num_used": 2,\
            "recurring": "T",\
            "email_id": "annrupp22@gmail.com",\
            "cup_business_uid": ""\
        },\
        {\
            "coupon_uid": "600-000003",\
            "coupon_id": "annfreedelivery",\
            "valid": "TRUE",\
            "discount_percent": 0,\
            "discount_amount": 0,\
            "discount_shipping": 0,\
            "expire_date": "2021-05-20",\
            "limits": 99,\
            "notes": "Free Delivey",\
            "num_used": 1,\
            "recurring": "T",\
            "email_id": "annrupp22@gmail.com",\
            "cup_business_uid": ""\
        },\
        {\
            "coupon_uid": "600-000011",\
            "coupon_id": "PJB08N",\
            "valid": "TRUE",\
            "discount_percent": 0,\
            "discount_amount": 0,\
            "discount_shipping": 0,\
            "expire_date": "2020-06-07",\
            "limits": 2,\
            "notes": "Coupon post from form",\
            "num_used": 3,\
            "recurring": "T",\
            "email_id": "",\
            "cup_business_uid": ""\
        },\
        {\
            "coupon_uid": "600-000013",\
            "coupon_id": "SNdiscount",\
            "valid": "TRUE",\
            "discount_percent": 0,\
            "discount_amount": 0,\
            "discount_shipping": 0,\
            "expire_date": "2021-05-20",\
            "limits": 99,\
            "notes": "$3 Discount",\
            "num_used": 1,\
            "recurring": "T",\
            "email_id": "",\
            "cup_business_uid": ""\
        },\
        {\
            "coupon_uid": "600-000014",\
            "coupon_id": "snfreed",\
            "valid": "TRUE",\
            "discount_percent": 0,\
            "discount_amount": 0,\
            "discount_shipping": 0,\
            "expire_date": "2021-05-20",\
            "limits": 90,\
            "notes": "Free Delivey",\
            "num_used": 10,\
            "recurring": "T",\
            "email_id": "",\
            "cup_business_uid": ""\
        }
    ]

###update_Coupons

[Post]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/update_Coupons/coupon_uid

example:    https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/update_Coupons/600-000001

return : code 200 if successful else 404 if coupon_uid doesn't exists


### purchase

[Post]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/purchase

input:

{\
"pur_customer_uid" : "100-000009",\
"pur_business_uid" : "200-000001",\
"items" : "[{\"qty\": \"1\", \"name\": \"5 Meal Plan - Weekly\", \"price\": \"59.99\", \"item_uid\": \"320-000002\"}]",\
"order_instructions" : "fast",\
"delivery_instructions" : "Keep Fresh",\
"order_type" : "meal",\
"delivery_first_name" : "xyz",\
"delivery_last_name" : "abc",\
"delivery_phone_num" : "6197872089",\
"delivery_email" : "xyz@gmail.com",\
"delivery_address" : "790 Carrywood Way",\
"delivery_unit" : "9",\
"delivery_city" : "San Jose",\
"delivery_state" : "CA",\
"delivery_zip" : "95120",\
"delivery_latitude" : "37.2271302",\
"delivery_longitude" : "-121.8891617",\
"purchase_notes" : "purchase_notes"\
}

NOTE: This endpoint checks email before entering the purchase information in database

return: code 200 if information updated successfully else any other code.


### payment

[post]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/payment

input:

{
"pay_purchase_uid" : "400-000035",\
"pay_purchase_id" : "400-000035",\
"start_delivery_date" : "2020-08-02 00:00:00",\
"pay_coupon_id" : "",\
"amount_due" : "53.75",\
"amount_discount" : "0",\
"amount_paid" : "53.75",\
"info_is_Addon" : "FALSE",\
"cc_num" : "4545",\
"cc_exp_date" : "2028-07-01 00:00:00",\
"cc_cvv" : "666",\
"cc_zip" : "99999",\
"charge_id" : "",\
"payment_type" : "STRIPE"\
}


return: code 200 if information updated successfully else any other code.


### history

[Get]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/history/email

example:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/history/abc@gmail.com

return: lastest 5 purchases by the user

{\
        "purchase_uid": "400-000307",\
        "purchase_date": "2020-09-20",\
        "purchase_id": "400-000307",\
        "purchase_status": "ACTIVE",\
        "pur_customer_uid": "100-000009",\
        "pur_business_uid": "200-000001",\
        "items": "[{\"qty\": \"1\",\ \"name\": \"5 Meal Plan - Weekly\",\ \"price\": \"59.99\",\ \"item_uid\": \"320-000002\"}]",\
        "order_instructions": "fast",\
        "delivery_instructions": "Keep Fresh",\
        "order_type": "meal",\
        "delivery_first_name": "xyz",\
        "delivery_last_name": "aad",\
        "delivery_phone_num": "6197872089",\
        "delivery_email": "abc@gmail.com",\
        "delivery_address": "790 Carrywood Way",\
        "delivery_unit": "9",\
        "delivery_city": "San Jose",\
        "delivery_state": "CA",\
        "delivery_zip": "95120",\
        "delivery_latitude": "37.2271302",\
        "delivery_longitude": "-121.8891617",\
        "purchase_notes": "purchase_notes",\
        "delivery_status": null,\
        "feedback_rating": 0,\
        "feedback_notes": null,\
        "payment_uid": "500-000102",\
        "payment_id": "500-000102",\
        "pay_purchase_uid": "400-000307",\
        "pay_purchase_id": "400-000307",\
        "payment_time_stamp": "2020-09-20",\
        "start_delivery_date": "2020-08-02",\
        "pay_coupon_id": "",\
        "amount_due": 53.75,\
        "amount_discount": 0,\
        "amount_paid": 53.75,\
        "info_is_Addon": "FALSE",\
        "cc_num": 4545,\
        "cc_exp_date": "2028-07-01",\
        "cc_cvv": "666",\
        "cc_zip": "99999",\
        "charge_id": "",\
        "payment_type": "STRIPE"\
    },\
    {\
        "purchase_uid": "400-000306",\
        "purchase_date": "2020-09-20",\
        "purchase_id": "400-000306",\
        "purchase_status": "ACTIVE",\
        "pur_customer_uid": "100-000009",\
        "pur_business_uid": "200-000001",\
        "items": "[{\"qty\": \"1\",\ \"name\": \"5 Meal Plan - Weekly\",\ \"price\": \"59.99\",\ \"item_uid\": \"320-000002\"}]",\
        "order_instructions": "fast",\
        "delivery_instructions": "Keep Fresh",\
        "order_type": "meal",\
        "delivery_first_name": "zzz",\
        "delivery_last_name": "xyz",\
        "delivery_phone_num": "6197872089",\
        "delivery_email": "abc@gmail.com",\
        "delivery_address": "790 Carrywood Way",\
        "delivery_unit": "9",\
        "delivery_city": "San Jose",\
        "delivery_state": "CA",\
        "delivery_zip": "95120",\
        "delivery_latitude": "37.2271302",\
        "delivery_longitude": "-121.8891617",\
        "purchase_notes": "purchase_notes",\
        "delivery_status": null,\
        "feedback_rating": 0,\
        "feedback_notes": null,\
        "payment_uid": "500-000101",\
        "payment_id": "500-000101",\
        "pay_purchase_uid": "400-000306",\
        "pay_purchase_id": "400-000306",\
        "payment_time_stamp": "2020-09-20",\
        "start_delivery_date": "2020-08-02",\
        "pay_coupon_id": "",\
        "amount_due": 53.75,\
        "amount_discount": 0,\
        "amount_paid": 53.75,\
        "info_is_Addon": "FALSE",\
        "cc_num": 4545,\
        "cc_exp_date": "2028-07-01",\
        "cc_cvv": "666",\
        "cc_zip": "99999",\
        "charge_id": "",\
        "payment_type": "STRIPE"\
    },\
    {\
        "purchase_uid": "400-000305",\
        "purchase_date": "2020-09-20",\
        "purchase_id": "400-000305",\
        "purchase_status": "ACTIVE",\
        "pur_customer_uid": "100-000009",\
        "pur_business_uid": "200-000001",\
        "items": "[{\"qty\": \"1\",\ \"name\": \"5 Meal Plan - Weekly\",\ \"price\": \"59.99\",\ \"item_uid\": \"320-000002\"}]",\
        "order_instructions": "fast",\
        "delivery_instructions": "Keep Fresh",\
        "order_type": "meal",\
        "delivery_first_name": "abc",\
        "delivery_last_name": "xyz",\
        "delivery_phone_num": "6197872089",\
        "delivery_email": "abc@gmail.com",\
        "delivery_address": "790 Carrywood Way",\
        "delivery_unit": "9",\
        "delivery_city": "San Jose",\
        "delivery_state": "CA",\
        "delivery_zip": "95120",\
        "delivery_latitude": "37.2271302",\
        "delivery_longitude": "-121.8891617",\
        "purchase_notes": "purchase_notes",\
        "delivery_status": null,\
        "feedback_rating": 0,\
        "feedback_notes": null,\
        "payment_uid": "500-000100",\
        "payment_id": "500-000100",\
        "pay_purchase_uid": "400-000305",\
        "pay_purchase_id": "400-000305",\
        "payment_time_stamp": "2020-09-20",\
        "start_delivery_date": "2020-08-02",\
        "pay_coupon_id": "",\
        "amount_due": 53.75,\
        "amount_discount": 0,\
        "amount_paid": 53.75,\
        "info_is_Addon": "FALSE",\
        "cc_num": 4545,\
        "cc_exp_date": "2028-07-01",\
        "cc_cvv": "666",\
        "cc_zip": "99999",\
        "charge_id": "",\
        "payment_type": "STRIPE"\
    },\
    {\
        "purchase_uid": "400-000304",\
        "purchase_date": "2020-09-19",\
        "purchase_id": "400-000304",\
        "purchase_status": "ACTIVE",\
        "pur_customer_uid": "100-000009",\
        "pur_business_uid": "200-000001",\
        "items": "[{\"qty\": \"1\",\ \"name\": \"5 Meal Plan - Weekly\",\ \"price\": \"59.99\",\ \"item_uid\": \"320-000002\"}]",\
        "order_instructions": "fast",\
        "delivery_instructions": "Keep Fresh",\
        "order_type": "meal",\
        "delivery_first_name": "abc",\
        "delivery_last_name": "xyz",\
        "delivery_phone_num": "6197872089",\
        "delivery_email": "abc@gmail.com",\
        "delivery_address": "790 Carrywood Way",\
        "delivery_unit": "9",\
        "delivery_city": "San Jose",\
        "delivery_state": "CA",\
        "delivery_zip": "95120",\
        "delivery_latitude": "37.2271302",\
        "delivery_longitude": "-121.8891617",\
        "purchase_notes": "purchase_notes",\
        "delivery_status": null,\
        "feedback_rating": 0,\
        "feedback_notes": null,\
        "payment_uid": "500-000099",\
        "payment_id": "500-000099",\
        "pay_purchase_uid": "400-000304",\
        "pay_purchase_id": "400-000304",\
        "payment_time_stamp": "2020-09-19",\
        "start_delivery_date": "2020-08-02",\
        "pay_coupon_id": "",\
        "amount_due": 53.75,\
        "amount_discount": 0,\
        "amount_paid": 53.75,\
        "info_is_Addon": "FALSE",\
        "cc_num": 4545,\
        "cc_exp_date": "2028-07-01",\
        "cc_cvv": "666",\
        "cc_zip": "99999",\
        "charge_id": "",\
        "payment_type": "STRIPE"\
    },\
    {\
        "purchase_uid": "400-000303",\
        "purchase_date": "2020-09-19",\
        "purchase_id": "400-000303",\
        "purchase_status": "ACTIVE",\
        "pur_customer_uid": "100-000009",\
        "pur_business_uid": "200-000001",\
        "items": "[{\"qty\": \"1\",\ \"name\": \"5 Meal Plan - Weekly\",\ \"price\": \"59.99\",\ \"item_uid\": \"320-000002\"}]",\
        "order_instructions": "fast",\
        "delivery_instructions": "Keep Fresh",\
        "order_type": "meal",\
        "delivery_first_name": "Parva",\
        "delivery_last_name": "Shah",\
        "delivery_phone_num": "6197872089",\
        "delivery_email": "abc@gmail.com",\
        "delivery_address": "790 Carrywood Way",\
        "delivery_unit": "9",\
        "delivery_city": "San Jose",\
        "delivery_state": "CA",\
        "delivery_zip": "95120",\
        "delivery_latitude": "37.2271302",\
        "delivery_longitude": "-121.8891617",\
        "purchase_notes": "purchase_notes",\
        "delivery_status": null,\
        "feedback_rating": 0,\
        "feedback_notes": null,\
        "payment_uid": "500-000098",\
        "payment_id": "500-000098",\
        "pay_purchase_uid": "400-000303",\
        "pay_purchase_id": "400-000303",\
        "payment_time_stamp": "2020-09-19",\
        "start_delivery_date": "2020-08-02",\
        "pay_coupon_id": "",\
        "amount_due": 53.75,\
        "amount_discount": 0,\
        "amount_paid": 53.75,\
        "info_is_Addon": "FALSE",\
        "cc_num": 4545,\
        "cc_exp_date": "2028-07-01",\
        "cc_cvv": "666",\
        "cc_zip": "99999",\
        "charge_id": "",\
        "payment_type": "STRIPE"\
    }




### purchase_Data_SF

[Post]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/purchase_Data_SF

Input :

{\
"pur_customer_uid" : "100-000009",\
"pur_business_uid" : "200-000001",\
"items" : "[{\"qty\": \"1\",\ \"name\": \"5 Meal Plan - Weekly\",\ \"price\": \"59.99\",\ \"item_uid\": \"320-000002\"}]",\
"order_instructions" : "fast",\
"delivery_instructions" : "Keep Fresh",\
"order_type" : "meal",\
"delivery_first_name" : "xyz",\
"delivery_last_name" : "aad",\
"delivery_phone_num" : "6197872089",\
"delivery_email" : "abc@gmail.com",\
"delivery_address" : "790 Carrywood Way",\
"delivery_unit" : "9",\
"delivery_city" : "San Jose",\
"delivery_state" : "CA",\
"delivery_zip" : "95120",\
"delivery_latitude" : "37.2271302",\
"delivery_longitude" : "-121.8891617",\
"purchase_notes" : "purchase_notes",\
"start_delivery_date" : "2020-08-02 00:00:00",\
"pay_coupon_id" : "",\
"amount_due" : "53.75",\
"amount_discount" : "0",\
"amount_paid" : "53.75",\
"info_is_Addon" : "FALSE",\
"cc_num" : "4545",\
"cc_exp_date" : "2028-07-01 00:00:00",\
"cc_cvv" : "666",\
"cc_zip" : "99999",\
"charge_id" : "",\
"payment_type" : "STRIPE"\
}

return: code 200 for successful insertion of data in purchase and payments table else 400 for error.


### addItems

[Post]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/addItems/input

example:

1. https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/addItems/Insert
2. https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/addItems/Update
3. https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/addItems/Status

INPUT:

For Insert ---

{\
"itm_business_uid" : "200-000009",\
"item_name" : "Grapes",\
"item_status" : "",\
"item_type" : "fruit",\
"item_desc" : "[organic,red,seedless]",\
"item_unit" : "lbs",\
"item_price" : "5.99",\
"item_sizes" : "M",\
"favorite" : "FALSE",\
"item_photo" : file, \ --- upload image file\
"exp_date" : ""\
}

For Update ---

{\
"itm_business_uid" : "200-000009",\
"item_name" : "Banana",\
"item_status" : "",\
"item_type" : "fruit",\
"item_desc" : "[organic,red,seedless]",\
"item_unit" : "lbs",\
"item_price" : "5.99",\
"item_sizes" : "M",\
"favorite" : "FALSE",\
"exp_date" : "",\
"item_uid" : "310-000208"\
}

For Status ---

{\
"item_uid" : "310-000208",\
"item_status" : "Past"\
}

return: code 200 for successful insertion of data in purchase and payments table else 400 for error.



### delivery_status

[Post]

This endpoint helps in changing delivery status of a purchase from not delivered to delivered


endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/addItems/purchase_uid

example:    https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/addItems/400-000001


### business_details_update

[Post]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/business_details_update/action

example:

1. https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/business_details_update/Get
2. https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/business_details_update/Post

Get request returns all business details of a specific business uid

Post request updates business details of a specific business uid

INPUT:

--Get--:

{
"business_uid" : "200-000004"
}

--Post--:

{
"business_uid" : "200-000001",\
"business_created_at" : "2020-01-09 17:34:48",\
"business_name" : "PTYD",\
"business_type" : "kriti",\
"business_desc" : "Vegan Delivery Service",\
"business_contact_first_name" : "Heather",\
"business_contact_last_name" : "Faiez",\
"business_phone_num" : "(512) 555-1234",\
"business_phone_num2" : "(512) 555-1200",\
"business_email" : "heather@ptyd.com",\
"business_hours" : "{"Friday": ["00:00:00", "23:59:00"], "Monday": ["00:00:00", "23:59:00"], "Sunday": ["00:00:00", "23:59:00"], "Tuesday": ["00:00:00", "23:59:00"], "Saturday": ["00:00:00", "23:59:00"]}",\
"business_accepting_hours" : "{"Friday": ["09:00:00", "23:59:59"], "Monday": ["09:00:00", "23:59:59"], "Sunday": ["09:00:00", "23:59:59"], "Tuesday": ["09:00:00", "23:59:59"], "Saturday": ["09:00:00", "21:00:00"], "Thursday": ["09:00:00", "23:59:59"], "Wednesday": ["09:00:00", "23:00:00"]}",\
"business_delivery_hours" : "{"Friday": ["09:00:00", "23:59:59"], "Monday": ["00:00:00", "00:00:00"], "Sunday": ["09:00:00", "23:59:59"], "Tuesday": ["09:00:00", "23:59:59"], "Saturday": ["09:00:00", "21:00:00"], "Thursday": ["09:00:00", "23:59:59"], "Wednesday": ["09:00:00", "23:00:00"]}",\
"business_address" :"360 Cowden Road",\
"business_unit" : "",\
"business_city" :  "Hollister",\
"business_state" : "CA",\
"business_zip" : "95135",\
"business_longitude" : "-121.9141246",\
"business_latitude" : "37.3316565",\
"business_EIN" : "",\
"business_WAUBI" : "",\
"business_license" : "",\
"business_USDOT" : "",\
"notification_approval" : "",\
"notification_device_id" : "",\
"can_cancel" : "0",\
"delivery" : "0",\
"reusable" : "0",\
"business_image" : "https://servingnow.s3-us-west-1.amazonaws.com/kitchen_imgs/landing-logo.png",\
"business_password" : "pbkdf2:sha256:150000$zMHfn0jt$29cef351d84456b5f6b665bc2bbab8ae3c6e42bd0e4a4e8967041a9455a24798"\
}

### orders_by_farm

[Get]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/orders_by_farm

Deconstructs items json object and outputs items ordered for a particular farm

Used in order details on farmer's report page

Return:

{
    "purchase_uid": "400-000331",\
    "purchase_date": "2020-09-23",\
    "purchase_id": "400-000331",\
    "purchase_status": "ACTIVE",\
    "pur_customer_uid": "100-000101",\
    "pur_business_uid": "",\
    "items": "[{"qty": "2", "name": "Squash", "price": "4", "item_uid": "310-000133", "itm_business_uid": "200-000006"}, {"qty": "4", "name": "Eggplant", "price": "3", "item_uid": "310-000135", "itm_business_uid": "200-000006"}]",\
    "order_instructions": "fast",\
    "delivery_instructions": "",\
    "order_type": "meal",\
    "delivery_first_name": "Zach",\
    "delivery_last_name": "Lind",\
    "delivery_phone_num": "9259840473",\
    "delivery_email": "zlind@ucsc.edu",\
    "delivery_address": "373 Western Drive",\
    "delivery_unit": "K",\
    "delivery_city": "Santa Cruz",\
    "delivery_state": "CA",\
    "delivery_zip": "94526",\
    "delivery_latitude": "0",\
    "delivery_longitude": "0",\
    "purchase_notes": "purchase_notes",\
    "delivery_status": null,
    "feedback_rating": 0,
    "feedback_notes": null,
    "qty": "2",\
    "name": "Squash",\
    "price": "4",\
    "item_uid": "310-000133",\
    "itm_business_uid": "200-000006",\
    "deconstruct.qty": "2",\
    "deconstruct.name": "Squash",\
    "deconstruct.price": "4",\
    "deconstruct.item_uid": "310-000133",\
    "deconstruct.itm_business_uid": "200-000006"\
},\
{\
    "purchase_uid": "400-000331",\
    "purchase_date": "2020-09-23",\
    "purchase_id": "400-000331",\
    "purchase_status": "ACTIVE",\
    "pur_customer_uid": "100-000101",\
    "pur_business_uid": "",\
    "items": "[{"qty": "2", "name": "Squash", "price": "4", "item_uid": "310-000133", "itm_business_uid": "200-000006"}, {"qty": "4", "name": "Eggplant", "price": "3", "item_uid": "310-000135", "itm_business_uid": "200-000006"}]",\
    "order_instructions": "fast",\
    "delivery_instructions": "",\
    "order_type": "meal",\
    "delivery_first_name": "Zach",\
    "delivery_last_name": "Lind",\
    "delivery_phone_num": "9259840473",\
    "delivery_email": "zlind@ucsc.edu",\
    "delivery_address": "373 Western Drive",\
    "delivery_unit": "K",\
    "delivery_city": "Santa Cruz",\
    "delivery_state": "CA",\
    "delivery_zip": "94526",\
    "delivery_latitude": "0",\
    "delivery_longitude": "0",\
    "purchase_notes": "purchase_notes",\
    "delivery_status": null,
    "feedback_rating": 0,
    "feedback_notes": null,
    "qty": "4",\
    "name": "Eggplant",\
    "price": "3",\
    "item_uid": "310-000135",\
    "itm_business_uid": "200-000006",\
    "deconstruct.qty": "4",\
    "deconstruct.name": "Eggplant",\
    "deconstruct.price": "3",\
    "deconstruct.item_uid": "310-000135",\
    "deconstruct.itm_business_uid": "200-000006"\
}


### orders_info

[Get]


endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/orders_info

Ouputs purchase info and amount due and paid which will help to deduce if payment is completed or not

Used at Report page in front

return:

 {\
            "purchase_uid": "400-000331"'\
            "purchase_date": "2020-09-23"'\
            "purchase_id": "400-000331"'\
            "purchase_status": "ACTIVE"'\
            "pur_customer_uid": "100-000101"'\
            "pur_business_uid": ""'\
            "items": "[{"qty": "2", "name": "Squash", "price": "4", "item_uid": "310-000133", "itm_business_uid": "200-000006"}, {"qty": "4", "name": "Eggplant", "price": "3", "item_uid": "310-000135", "itm_business_uid": "200-000006"}]",\
            "order_instructions": "fast"'\
            "delivery_instructions": ""'\
            "order_type": "meal"'\
            "delivery_first_name": "Zach"'\
            "delivery_last_name": "Lind"'\
            "delivery_phone_num": "9259840473"'\
            "delivery_email": "zlind@ucsc.edu"'\
            "delivery_address": "373 Western Drive"'\
            "delivery_unit": "K"'\
            "delivery_city": "Santa Cruz"'\
            "delivery_state": "CA"'\
            "delivery_zip": "94526"'\
            "delivery_latitude": "0"'\
            "delivery_longitude": "0"'\
            "purchase_notes": "purchase_notes"'\
            "delivery_status": null,\
            "feedback_rating": 0,\
            "feedback_notes": null,\
            "amount_due": 21.2,\
            "amount_paid": 21.2\
        }






