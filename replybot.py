"""
Bot that sends a given reply for each message in a stream
"""

import zulipclient

class ReplyBot(object):
    def __init__(self, email, api_key, stream="test-bot", message="oyo!"):
        self.client = zulipclient.ZulipClient(email, api_key)
        self.stream = stream
        self.message = message

    def subscibe(self):
        self.client.subscibe_to_streams(self.stream)

    def on_message(self):
        self.client.send_message(message_type="stream", subject="Babar", to=self.stream, content=self.message)



if __name__ == '__main__':

    from os import environ

    email = environ['zulip_email']
    api_key = environ['zulip_key']

    a_bot = ReplyBot(email, api_key)
    a_bot.on_message()

