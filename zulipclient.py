from __future__ import print_function
from __future__ import unicode_literals

import requests


class ZulipCient(object):

    zulip_api_url = "https://api.zulip.com/v1/{0}"
    zulip_api_message = zulip_api_url.format("messages")
    zulip_api_register = zulip_api_url.format("register")
    zulip_api_events = zulip_api_url.format("events")

    event_types = {"message", "subscriptions", "realm_user", "pointer"}

    def __init__(self, email, api_key):
        self.email = email
        self.api_key = api_key
        self.bot_auth = (self.email, self.api_key)

    def send_message(self, **kwargs):
        # type is a python keyword
        kwargs["type"] = kwargs.pop("message_type")
        print(kwargs)
        r = requests.post(self.zulip_api_message, params=kwargs, auth=self.bot_auth)
        resp = r.json()
        print(resp["result"])
        # replace that with a function and a try? if "result" not in rep...
        if resp["result"] == "success": # we should use a try
            print("Message sent", kwargs)
        else:
            print("Send message error")
            print(resp)

    def subscribe_to_streams(self, streams):
        streams = str(streams).replace("'", '"') # must use double quotes in interior of list
        assert streams.startswith('["')
        params = {"add" : streams}
        r = requests.patch(self.zulip_api_url, params=params, auth=self.bot_auth)
        resp = r.json()
        if resp["result"] == "success":
            print("Subscribed to streams", streams)
        else:
            print("Subscription error")
            print(resp)

    def register_queue(self, *events):
        assert self.event_type.issuperset(set(events))
        events = str(events).replace("'", '"') # must use double quotes in interior of list
        assert events.startswith('["')
        params = {"event_types": events}
        r = requests.post(self.zulip_api_register, params=params, auth=self.bot_auth)
        resp = r.json()
        if resp["result"] == "success": # we should use a try
            print("Regisered to ", events)
        else:
            print("Send message error")
            print(resp)

    def get_event(self, queue_id):
        params = {"queue_id": queue_id,  "last_event_id": -1}
        r = requests.get(self.zulip_api_events, params=params, auth=self.bot_auth)
        resp = r.json()
        return resp

if __name__ == '__main__':

    from os import environ

    email = environ['zulip_email']
    api_key = environ['zulip_key']

    client = ZulipCient(email, api_key)
    r = client.register_queue('message')
    print(r)
    queue_id = r['queue_id']
    print(client.get_event(queue_id))
    #client.send_message(message_type="private",\
                    #to="allison@hackerschool.com",\
                    #content="Yes")


