"""
"""

import logging
import random
import time

from google.appengine.ext import ndb, deferred
from google.appengine.api import memcache


MEMCACHE_NS = '_sub'



class Subscribers(ndb.Model):
    """
    @parent: None
    @key_name: name of the item being subscribed
    """

    channels = ndb.PickleProperty()

    @classmethod
    def build_key(cls, name):
        return ndb.Key(cls, name)



def subscribe(name, channel_id):
    client = memcache.Client()

    memcache_key = unicode(name, 'utf-8')
    sub_key = Subscribers.build_key(name)

    while True:
        channel_ids = client.gets(memcache_key, namespace=MEMCACHE_NS)
        new = channel_ids is None

        if channel_ids is None:
            sub_entity = sub_key.get()

            channel_ids = sub_entity.channels if sub_entity else []

        channel_ids.append(channel_id)

        channel_ids = list(set(channel_ids))

        if new and client.set(memcache_key, channel_ids, namespace=MEMCACHE_NS):
            break
        elif client.cas(memcache_key, channel_ids, namespace=MEMCACHE_NS):
            break

        time.sleep(random.random() * 0.05)

    # enqueue a task that will persist this new value

    if memcache.add(memcache_key + '_dirty', 1, namespace=MEMCACHE_NS):
        deferred.defer(flush, name)



def unsubscribe(name, channel_id):
    client = memcache.Client()

    memcache_key = unicode(name, 'utf-8')
    sub_key = Subscribers.build_key(name)

    while True:
        channel_ids = client.gets(memcache_key, namespace=MEMCACHE_NS)
        new = channel_ids is None

        if channel_ids is None:
            sub_entity = sub_key.get()

            channel_ids = sub_entity.channels if sub_entity else []

        try:
            channel_ids.remove(channel_id)
        except ValueError:
            return

        channel_ids = list(set(channel_ids))

        if new and client.set(memcache_key, channel_ids, namespace=MEMCACHE_NS):
            break
        elif client.cas(memcache_key, channel_ids, namespace=MEMCACHE_NS):
            break

        time.sleep(random.random() * 0.05)

    # enqueue a task that will persist this new value

    if memcache.add(memcache_key + '_dirty', 1, namespace=MEMCACHE_NS):
        deferred.defer(flush, name)



def flush(name):
    """
    Flush the cached audience list to the datastore.
    """
    memcache_key = unicode(name, 'utf-8')

    channel_ids = memcache.get(memcache_key)

    if channel_ids is None:
        logging.critical('Cache fail for reading subscribers for %r' % (name,))
        memcache.delete(memcache_key + '_dirty', namespace=MEMCACHE_NS)

        return

    sub_key = Subscribers.build_key(name)

    @ndb.transactional
    def txn():
        sub_entity = sub_key.get()

        if not sub_entity:
            sub_entity = Subscribers(key=sub_key)

        orig_channels = sub_entity.channels or []

        sub_entity.channels = channel_ids

        sub_entity.put()

        return orig_channels

    try:
        orig_channels = txn()
    finally:
        memcache.delete(memcache_key + '_dirty', namespace=MEMCACHE_NS)

    orig_channels = set(orig_channels)

    # work out the diff between the two lists
    added = list(channel_ids.difference(orig_channels))
    removed = list(orig_channels.difference(channel_ids))

    logging.info('flush result added: %r, removed %r', added, removed)



def get_subscribers(name):
    if isinstance(name, unicode):
        memcache_key = name.encode('utf-8')
    else:
        memcache_key = unicode(name, 'utf-8')

    channel_ids = memcache.get(memcache_key, namespace=MEMCACHE_NS)

    if channel_ids is not None:
        return channel_ids

    # memcache failure, try from the datastore
    sub_key = Subscribers.build_key(name)
    sub_entity = sub_key.get()

    channel_ids = sub_entity.channels if sub_entity else []

    memcache.set(memcache_key, channel_ids or [], namespace=MEMCACHE_NS)

    return channel_ids
