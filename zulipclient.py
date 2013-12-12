"""
Python bindings for the Zulip API
https://zulip.com/api/
"""

import requests
import json

import tornado
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.httputil import url_concat

class ZulipClient(object):

    zulip_api_endpoint = "https://api.zulip.com/v1/{0}"
    zulip_api_message = zulip_api_endpoint.format("messages")
    zulip_api_register = zulip_api_endpoint.format("register")
    zulip_api_events = zulip_api_endpoint.format("events")

    event_types = {"message", "subscriptions", "realm_user", "pointer"}

    def __init__(self, email, api_key):
        self.email = email
        self.api_key = api_key
        self.bot_auth = (self.email, self.api_key)
        self.http_client = AsyncHTTPClient()

    def subscribe_to_streams(self, *streams):
        # Zulip needs this list format
        streams = json.dumps(list(streams))
        params = {"add" : streams}
        r = requests.patch(self.zulip_api_endpoint, params=params, auth=self.bot_auth)
        resp = r.json()
        if resp["result"] == "success":
            streams_str = str(streams)[1:-1] # remove the parenthesis
            print("Subscribed to streams {0}.".format(streams_str))
        else:
            print("Subscription error")
            print(resp)

    def register_queue(self, *events):
        if not self.event_types.issuperset(set(events)):
            raise KeyError
        # Zulip needs this list format
        events = json.dumps(list(events))
        params = {"event_types": events}
        r = requests.post(self.zulip_api_register, params=params, auth=self.bot_auth)
        resp = r.json()
        if resp["result"] == "success": # we should use a try
            events_str = str(events)[1:-1] # remove the parenthesis
            print("Subscribed to queue {0}.".format(events_str))
            return (resp['queue_id'], resp['last_event_id'])
        else:
            print("Send message error")
            print(resp)

    def get_event(self, queue_id):
        params = {"queue_id": queue_id,  "last_event_id": -1}
        r = requests.get(self.zulip_api_events, params=params, auth=self.bot_auth)
        resp = r.json()
        return resp

    def call_on_each(self):
        pass
    # cf zulip python bindings
    # register a chaque event?

    def get(self, path, params=None):
        pass

    def send_message(self, **params):
        # type is a python keyword
        r = requests.post(self.zulip_api_message, params=params, auth=self.bot_auth)
        resp = r.json()
        # replace that with a function and a try? if "result" not in rep...
        if resp["result"] == "success": # we should use a try
            print("Message sent", params)
        else:
            print("Send message error")
            print(resp)

    def send_strean_msg(self):
        pass

    def handle_request(self, response):
        if response.error:
            print("Error", response)
        else:
            print(response.body)


    def post(self, url, params):
        path  = url_concat(url, params)
        request = HTTPRequest(url=path,
                              method='POST',
                              body = "", # bad error otherwise
                              auth_username=self.email,
                              auth_password=self.api_key)
        return self.http_client.fetch(request, self.handle_request)

    def simple_request(self):
        self.http_client.fetch("http://requestb.in/1kghftd1", callback=self.simple_callback)

    def simple_callback(self, response):
        print response

    def send_private_msg(self, to, content):
        params = {'type':'private', 'to': to, 'content': content}
        return self.post(self.zulip_api_message, params)



if __name__ == '__main__':

    from os import environ

    email = environ['zulip_email']
    api_key = environ['zulip_key']
    client = ZulipClient(email, api_key)

    #client.send_message(type="private",
                        #to="denisgarci@gmail.com",
                        #content="ancienne methode")

    a = client.send_private_msg("denisgarci@gmail.com",
                            "Hey, Just to let you know I'm having my code completely migrated to Tornado, and this is you first message of many async messages! :)")
    tornado.ioloop.IOLoop.instance().start()


