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
"password": "work123"\
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

endpoint:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/AccountSalt/<email>

example:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/AccountSalt/xyz@gmail.com

return: password_algorithm and password_salt

NOTE:

Use this endpoint only if user logins with email and password


### Login

[Post]

endpoint: https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Login/

input:

{
"email" : "annrupp22@gmail.com",\
"password" : "4178980d28dcec5b36521c1a9beeef791db4e6674aa77",\
"token" : ""\
}

return:

[\
        {\
            "customer_uid": "100-000005",\
            "customer_last_name": "Rupp",\
            "customer_first_name": "Ann",\
            "customer_email": "annrupp22@gmail.com",\
            "user_social_media": "NULL",\
            "user_access_token": "NULL",\
            "user_refresh_token": "NULL"\
        }\
    ]

NOTE:

email is necessary in fields but you can pass either hashed_password generated at front end or refresh token


### Profile

[Get]


endpoint: https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Profile/<email>

example:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Profile/xyz@gmail.com

return: all the details about customer


### getItems

[Get]

endpoint:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/getItems/<day>

example: https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/getItems/Monday


return: information of all items available at particular day

 "item_uid","created_at","itm_business_uid","item_name","item_status",\
 "item_type","item_desc","item_unit","item_price","item_sizes","favorite",\
 "item_photo","exp_date","business_delivery_hours"


### Refund

[Post]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/Refund

input: {"image_url":"http://servingnow.me","email":"abc@gmail.com","note":"Please issue a refund for eggplant" }

return: code either 200 or 400. If 200 refund ticket generated else email doesn't exists


### available_Coupons

[Get]

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/available_Coupons/<email>

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

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/update_Coupons/<coupon_uid>

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

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/history/<email>

example:  https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/history/tazi.arthur@hotmail.com

return: lastest 5 purchases by the user

{
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
        "payment_type": "STRIPE"
    },\
    {
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
        "payment_type": "STRIPE"
    },\
    {
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
        "payment_type": "STRIPE"
    },\
    {
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
        "payment_type": "STRIPE"
    },\
    {
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
        "payment_type": "STRIPE"
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

endpoint:   https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/addItems/<input>

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
"item_photo" : "https://s3-us-west-1.amazonaws.com/servingnow/meals_imgs/1e43591331714bdea715e8f50fb5d625_e1d73947e70541439bab8b95b2a07b07",\
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
"item_photo" : "https://s3-us-west-1.amazonaws.com/servingnow/meals_imgs/1e43591331714bdea715e8f50fb5d625_e1d73947e70541439bab8b95b2a07b07",\
"exp_date" : "",\
"item_uid" : "310-000208"\
}

For Status ---

{\
"item_uid" : "310-000208",\
"item_status" : "Past"\
}

return: code 200 for successful insertion of data in purchase and payments table else 400 for error.








