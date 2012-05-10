"""
"""

import logging

from google.appengine.api import channel
from google.appengine.ext import deferred


channel_service = channel.channel._GetService()



def dispatch_events(name, *events):
    payloads = []

    for event in events:
        payloads.append(event)

    if not payloads:
        logging.info('No messages for this batch run (weird?)')

        return

    deferred.defer(push_message, name, '{"messages": [%s]}' % ','.join(payloads))



def push_message(name, json_payload):
    from . import sub

    channel_ids = sub.get_subscribers(name)

    rpcs = []

    for channel_id in channel_ids:
        rpc = async_send_message(channel_id, json_payload)

        rpcs.append(rpc)

    logging.info(rpcs)




def async_send_message(client_id, message, callback=None):
    """
    The AppEngine SDK does not expose an asynchronous API for sending messages
    so we have to do it ourselves.

    @param client_id: The channel token
    @param message:
    @return:
    """
    from google.appengine.api import api_base_pb, apiproxy_stub_map

    client_id = channel.channel._ValidateClientId(client_id)

    if isinstance(message, unicode):
        message = message.encode('utf-8')
    elif not isinstance(message, str):
        raise channel.InvalidMessageError

    if len(message) > channel.MAXIMUM_MESSAGE_LENGTH:
        raise channel.InvalidMessageError

    request = channel.channel_service_pb.SendMessageRequest()
    response = api_base_pb.VoidProto()

    request.set_application_key(client_id)
    request.set_message(message)

    rpc = apiproxy_stub_map.CreateRPC(channel_service)

    rpc.MakeCall(channel_service, 'SendChannelMessage', request, response,
        callback=callback)

    return rpc
