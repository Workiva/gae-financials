"""
"""

import json



def subscribe(name, channel_id):
    from . import sub

    sub.subscribe(name, channel_id)



def unsubscribe(name, channel_id):
    from . import sub

    sub.unsubscribe(name, channel_id)



def send(name, event):
    """
    @param event: A JSONifiable object
    """
    from . import batch

    batch.add_event(name, json.dumps(event))
