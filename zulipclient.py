from __future__ import print_function
from __future__ import unicode_literals

import requests


class ZulipCient(object):

    zulip_api_url = "https://api.zulip.com/v1/messages"

    def __init__(self, email, api_key):
        self.email = email
        self.api_key = api_key
        self.bot_auth = (self.email, self.api_key)

    def send_message(self, **kwargs):
        # type is a python keyword
        kwargs["type"] = kwargs.pop("message_type")
        print(kwargs)
        r = requests.post(self.zulip_api_url, params=kwargs, auth=self.bot_auth)
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


if __name__ == '__main__':

    from os import environ

    email = environ['zulip_email']
    api_key = environ['zulip_key']

    client = ZulipCient(email, api_key)
    client.send_message(message_type="private",\
                        to="denisgarci@gmail.com",\
                        content="Salut c'est Babar.")


