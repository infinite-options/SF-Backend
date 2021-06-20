import time
import hmac
import base64
import hashlib
import json
import urllib.parse
import http.client


class Notification:
    def __init__(self, notification_format=None, payload=None, debug=0):
        valid_formats = ['template', 'apple', 'gcm', 'windows', 'windowsphone', "adm", "baidu"]
        if not any(x in notification_format for x in valid_formats):
            raise Exception(
                "Invalid Notification format. " +
                "Must be one of the following - 'template', 'apple', 'gcm', 'windows', 'windowsphone', 'adm', 'baidu'")

        self.format = notification_format
        self.payload = payload

        # array with keynames for headers
        # Note: Some headers are mandatory: Windows: X-WNS-Type, WindowsPhone: X-NotificationType
        # Note: For Apple you can set Expiry with header: ServiceBusNotification-ApnsExpiry
        # in W3C DTF, YYYY-MM-DDThh:mmTZD (for example, 1997-07-16T19:20+01:00).
        self.headers = None


class NotificationHub:
    API_VERSION = "?api-version=2013-10"
    DEBUG_SEND = "&test"

    def __init__(self, connection_string=None, hub_name=None, debug=0):
        self.HubName = hub_name
        self.Debug = debug
        #connection_string =
        #self.HubName =


        # Parse connection string
        parts = connection_string.split(';')
        if len(parts) != 3:
            raise Exception("Invalid ConnectionString.")

        for part in parts:
            if part.startswith('Endpoint'):
                self.Endpoint = 'https' + part[11:]
            if part.startswith('SharedAccessKeyName'):
                self.SasKeyName = part[20:]
            if part.startswith('SharedAccessKey'):
                self.SasKeyValue = part[16:]

    @staticmethod
    def get_expiry():
        # By default returns an expiration of 5 minutes (=300 seconds) from now
        return int(round(time.time() + 300))

    @staticmethod
    def encode_base64(data):
        return base64.b64encode(data)

    def sign_string(self, to_sign):
        key = self.SasKeyValue.encode('utf-8')
        to_sign = to_sign.encode('utf-8')
        signed_hmac_sha256 = hmac.HMAC(key, to_sign, hashlib.sha256)
        digest = signed_hmac_sha256.digest()
        encoded_digest = self.encode_base64(digest)
        return encoded_digest

    def generate_sas_token(self):
        target_uri = self.Endpoint + self.HubName
        my_uri = urllib.parse.quote(target_uri, '').lower()
        expiry = str(self.get_expiry())
        to_sign = my_uri + '\n' + expiry
        signature = urllib.parse.quote(self.sign_string(to_sign))
        auth_format = 'SharedAccessSignature sig={0}&se={1}&skn={2}&sr={3}'
        sas_token = auth_format.format(signature, expiry, self.SasKeyName, my_uri)
        return sas_token

    def make_http_request(self, url, payload, headers):
        parsed_url = urllib.parse.urlparse(url)
        connection = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port)

        if self.Debug > 0:
            connection.set_debuglevel(self.Debug)
            # adding this querystring parameter gets detailed information about the PNS send notification outcome
            url += self.DEBUG_SEND
            #print("--- REQUEST ---")
            #print("URI: " + url)
            #print("Headers: " + json.dumps(headers, sort_keys=True, indent=4, separators=(' ', ': ')))
            #print("--- END REQUEST ---\n")

        connection.request('POST', url, payload, headers)
        response = connection.getresponse()

        if self.Debug > 0:
            # #print out detailed response information for debugging purpose
            print("\n\n--- RESPONSE ---")
            print(str(response.status) + " " + response.reason)
            print(response.msg)
            print(response.read())
            print("--- END RESPONSE ---")

        elif response.status != 201:
            # Successful outcome of send message is HTTP 201 - Created
            raise Exception(
                "Error sending notification. Received HTTP code " + str(response.status) + " " + response.reason)

        connection.close()

    def get_all_registrations_with_a_tag(self, tag):
        url = self.Endpoint + self.HubName + '/tags/' + tag + '/registrations' + self.API_VERSION
        parsed_url = urllib.parse.urlparse(url)
        connection = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port)

        # if self.Debug > 0:
        #     connection.set_debuglevel(self.Debug)
        #     # adding this querystring parameter gets detailed information about the PNS send notification outcome
        #     url += self.DEBUG_SEND
        #     #print("--- REQUEST ---")
        #     #print("URI: " + url)
        #     #print("Headers: " + json.dumps(headers, sort_keys=True, indent=4, separators=(' ', ': ')))
        #     #print("--- END REQUEST ---\n")
        headers = {
            'Authorization': self.generate_sas_token(),
            'x-ms-version': '2015-01'
        }
        payload = ''
        connection.request('GET', url, payload, headers)
        response = connection.getresponse()
        return response
        #print("\n\n--- RESPONSE ---")
        #print(str(response.status) + " " + response.reason)
        #print(response.msg)
        #print("read:")
        ##print(response.read())
        #print("--- END RESPONSE ---")
        return str(response.read())

    def create_or_update_registration_android(self, registration_id, GCM_registration_id, tags):
        url = self.Endpoint + self.HubName + '/registrations/' + registration_id + self.API_VERSION
        parsed_url = urllib.parse.urlparse(url)
        connection = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port)

        headers = {
            'Content-Type': 'application/atom+xml;type=entry;charset=utf-8',
            'Authorization': self.generate_sas_token(),
            'x-ms-version': '2015-01'
        }
        body = f'''<?xml version="1.0" encoding="utf-8"?>
                    <entry xmlns="http://www.w3.org/2005/Atom">
                        <content type="application/xml">
                            <GcmRegistrationDescription xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/netservices/2010/10/servicebus/connect">
                                <Tags>{tags}</Tags>
                                <GcmRegistrationId>{GCM_registration_id}</GcmRegistrationId> 
                            </GcmRegistrationDescription>
                        </content>
                    </entry>'''
        connection.request('PUT', url, body, headers)
        response = connection.getresponse()
        return response
        #print("\n\n--- RESPONSE ---")
        #print(str(response.status) + " " + response.reason)
        #print(response.msg)
        #print(response.read())
        #print("--- END RESPONSE ---")

    def create_or_update_registration_iOS(self, registration_id, device_token, tags):
        url = self.Endpoint + self.HubName + '/registrations/' + registration_id + self.API_VERSION
        parsed_url = urllib.parse.urlparse(url)
        connection = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port)

        headers = {
            'Content-Type': 'application/atom+xml;type=entry;charset=utf-8',
            'Authorization': self.generate_sas_token(),
            'x-ms-version': '2015-01'
        }
        body = f'''<?xml version="1.0" encoding="utf-8"?>
                    <entry xmlns="http://www.w3.org/2005/Atom">
                        <content type="application/xml">
                            <AppleRegistrationDescription xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/netservices/2010/10/servicebus/connect">
                                <Tags>{tags}</Tags>
                                <DeviceToken>{device_token}</DeviceToken> 
                            </AppleRegistrationDescription>
                        </content>
                    </entry>'''
        connection.request('PUT', url, body, headers)
        response = connection.getresponse()
        return response

    def send_notification(self, notification, tag_or_tag_expression=None):
        url = self.Endpoint + self.HubName + '/messages' + self.API_VERSION

        json_platforms = ['template', 'apple', 'gcm', 'adm', 'baidu']

        if any(x in notification.format for x in json_platforms):
            content_type = "application/json"
            payload_to_send = json.dumps(notification.payload)
        else:
            content_type = "application/xml"
            payload_to_send = notification.payload

        headers = {
            'Content-type': content_type,
            'Authorization': self.generate_sas_token(),
            'ServiceBusNotification-Format': notification.format
        }

        if isinstance(tag_or_tag_expression, set):
            tag_list = ' || '.join(tag_or_tag_expression)
        else:
            tag_list = tag_or_tag_expression

        # add the tags/tag expressions to the headers collection
        if tag_list != "":
            headers.update({'ServiceBusNotification-Tags': tag_list})

        # add any custom headers to the headers collection that the user may have added
        if notification.headers is not None:
            headers.update(notification.headers)

        self.make_http_request(url, payload_to_send, headers)

    def send_apple_notification(self, payload, tags=""):
        nh = Notification("apple", payload)
        self.send_notification(nh, tags)

    def send_gcm_notification(self, payload, tags=""):
        nh = Notification("gcm", payload)
        self.send_notification(nh, tags)

    def send_adm_notification(self, payload, tags=""):
        nh = Notification("adm", payload)
        self.send_notification(nh, tags)

    def send_baidu_notification(self, payload, tags=""):
        nh = Notification("baidu", payload)
        self.send_notification(nh, tags)

    def send_mpns_notification(self, payload, tags=""):
        nh = Notification("windowsphone", payload)

        if "<wp:Toast>" in payload:
            nh.headers = {'X-WindowsPhone-Target': 'toast', 'X-NotificationClass': '2'}
        elif "<wp:Tile>" in payload:
            nh.headers = {'X-WindowsPhone-Target': 'tile', 'X-NotificationClass': '1'}

        self.send_notification(nh, tags)

    def send_windows_notification(self, payload, tags=""):
        nh = Notification("windows", payload)

        if "<toast>" in payload:
            nh.headers = {'X-WNS-Type': 'wns/toast'}
        elif "<tile>" in payload:
            nh.headers = {'X-WNS-Type': 'wns/tile'}
        elif "<badge>" in payload:
            nh.headers = {'X-WNS-Type': 'wns/badge'}

        self.send_notification(nh, tags)

    def send_template_notification(self, properties, tags=""):
        nh = Notification("template", properties)
        self.send_notification(nh, tags)





#hub.create_or_update_registration('7678985146758001737-6189004290585846588-1','E7F2BFA9E2EA84AC2AA6C057F1E16804CEAD7C5C7812402A76EB28020B8D42C9','default,ios,howard')
#hub.get_all_registrations_with_a_tag('guid_2bfd6f49-dc53-4ece-b38d-1ba729f7ec4c')
#hub.create_or_update_registration('7587903074845162734-3021491851548156642-3','E7F2BFA9E2EA84AC2AA6C057F1E16804CEAD7C5C7812402A76EB28020B8D42C9','som')
#wns_payload = """<toast><visual><binding template=\"ToastText01\"><text id=\"1\">Python Test</text></binding></visual></toast>"""
#hub.send_windows_notification(wns_payload)

# iOS payload format
# https://docs.microsoft.com/en-us/previous-versions/azure/reference/dn223266%28v%3dazure.100%29
# alert_payload = {
#     "aps" : {
#         "alert" : "Test message from backend for iOS!",
#     },
# }
# hub.send_apple_notification(alert_payload, tags = "default")

# fcm_payload = {
#     "data":{"message":"Test message from backend for Android!"}
# }
# hub.send_gcm_notification(fcm_payload, tags = "default")
