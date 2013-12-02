"""
Python bindings for the Zulip API
https://zulip.com/api/
"""

import requests
import json

class ZulipClient(object):

    zulip_api_url = "https://api.zulip.com/v1/{0}"
    zulip_api_message = zulip_api_url.format("messages")
    zulip_api_register = zulip_api_url.format("register")
    zulip_api_events = zulip_api_url.format("events")

    event_types = {"message", "subscriptions", "realm_user", "pointer"}

    def __init__(self, email, api_key):
        self.email = email
        self.api_key = api_key
        self.bot_auth = (self.email, self.api_key)

    def send_message(self, **params):
        # type is a python keyword
        params["type"] = params.pop("message_type")
        print(params)
        r = requests.post(self.zulip_api_message, params=params, auth=self.bot_auth)
        resp = r.json()
        # replace that with a function and a try? if "result" not in rep...
        if resp["result"] == "success": # we should use a try
            print("Message sent", params)
        else:
            print("Send message error")
            print(resp)

    def subscribe_to_streams(self, *streams):
        # Zulip needs this list format
        streams = json.dumps(list(streams))
        params = {"add" : streams}
        r = requests.patch(self.zulip_api_url, params=params, auth=self.bot_auth)
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

if __name__ == '__main__':

    from os import environ

    email = environ['zulip_email']
    api_key = environ['zulip_key']

    client = ZulipClient(email, api_key)
    #r = client.register_queue('message')
    #print(r)
    #queue_id = r['queue_id']
    #print(client.get_event(queue_id))
    client.send_message(message_type="private",\
                    to="denisgarci@gmail.com",\
                    content="")


