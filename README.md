zulipbot
========

A simple Zulip bot using my own Python bindings.
https://zulip.com/api/

Examples
--------

```
from zulipclient import ZulipClient

client = ZulipClient(email, api_key)
client.send_message(message_type="private",\
                    to="email@example.com",\
                    content="Hey there")
```

Status
------
Sending messages and subscribing to a stream works.

TODO
----
- Add support for async events (on-each) using Twisted.

- Finish working on the reply bot.

- Add a listener bot.

- Add a Markov sentence generator.

- Create an "alike" bot using the sentence generator.

