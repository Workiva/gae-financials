"""
So the idea is to do as many operations in batch as possible, using memcache
to store the context of the events produced by the front end requests.

Each room has a queue of events which these queues are processed in parallel
(also independant)
"""

import logging

from google.appengine.api import memcache
from google.appengine.ext import deferred



MEMCACHE_PREFIX = 'eq'
MEMCACHE_NS = '_event'
EVENT_TIMEOUT = 60 * 10
LOCK_TIMEOUT = 60



def _make_memcache_key(type_, *args):
    id_ = '-'.join(map(str, args))

    return "%s:%s:%s" % (MEMCACHE_PREFIX, type_, id_)



def get_head_key(*args):
    """
    Gets the memcache key that holds the HEAD pointer
    """
    return _make_memcache_key('H', *args)



def get_tail_key(*args):
    """
    Gets the memcache key that holds the TAIL pointer
    """
    return _make_memcache_key('T', *args)



def get_lock_key(*args):
    """
    Gets the memcache key that we use to indicate that the queue is dirty, and
    the batch processing deferred task needs to run
    """
    return _make_memcache_key('L', *args)



def get_event_key(*args):
    """
    Gets the memcache key for the data for a single event
    """
    return _make_memcache_key('E', *args)



def add_event(name, details):
    """
    Add a single event to the queue in memcache, incrementing the value at
    the HEAD pointer.
    """
    mkey = get_head_key(name)

    idx = memcache.incr(mkey, delta=1, initial_value=0, namespace=MEMCACHE_NS)

    ekey = get_event_key(name, idx)

    memcache.set(ekey, details, time=EVENT_TIMEOUT, namespace=MEMCACHE_NS)

    lock_key = get_lock_key(name)

    if memcache.add(lock_key, 1, time=LOCK_TIMEOUT, namespace=MEMCACHE_NS):
        deferred.defer(process_events, name)



def process_events(name):
    """
    This method processes all of the events.
    """
    tail_key = get_tail_key(name)
    lock_key = get_lock_key(name)

    while True:
        new_head, events = _list_outstanding_events(name)

        if not events:
            memcache.delete(lock_key, namespace=MEMCACHE_NS)

            return

        batch_size = 5
        while events:
            send_group = events[:batch_size]
            events = events[batch_size:]
            try:
                dispatch_events(name, *send_group)
            except Exception:
                logging.exception('Attempting to dispatch %r' % (send_group,))

        memcache.set(lock_key, 1, time=LOCK_TIMEOUT, namespace=MEMCACHE_NS)
        memcache.set(tail_key, new_head, namespace=MEMCACHE_NS)



def _list_outstanding_events(name):
    """
    Returns a list of all of the events in the queue that still need to be
    processed
    """
    head_key = get_head_key(name)
    tail_key = get_tail_key(name)

    idx_dict = memcache.get_multi([head_key, tail_key], namespace=MEMCACHE_NS)

    head_idx = idx_dict.get(head_key)
    tail_idx = idx_dict.get(tail_key)

    if head_idx is None:
        # memcache failure
        return 0, []

    if not tail_idx:
        tail_idx = 0

    if head_idx == tail_idx:
        return head_idx, []

    event_keys = []

    for idx in range(tail_idx + 1, head_idx + 1):
        event_keys.append(get_event_key(name, idx))

    events = memcache.get_multi(event_keys, namespace=MEMCACHE_NS)

    out = []

    for k in event_keys:
        event = events.get(k)

        if event:
            out.append(event)

    return head_idx, out



def dispatch_events(name, *events):
    from .push import dispatch_events

    dispatch_events(name, *events)
