#!/usr/bin/env python
#
# Copyright 2012 Ezox Systems LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Service endpoint mapping.

If this file gets large (say over 500 hundred lines), we suggest breaking
it up into a package.
"""

import json
import logging
from google.appengine.api import users
import webapp2
import event
from person import Person


class PersonHandler(webapp2.RequestHandler):
    def get(self):
        from appname.person import Person
        user_query = self.request.get('query')
        limit = int(self.request.get('limit', 40))

        query = Person.query(namespace="")
        if user_query:
            search = user_query.strip().lower()
            query = query.filter(Person.n_ >= search)
            query = query.filter(Person.n_ < search + u"\uFFFD")

        if limit > 0:
            query = query.fetch(limit)

        out = [entity.to_dict() for entity in query]
        self.response.out.write(json.dumps(out))

    def delete(self):
        from google.appengine.ext import ndb
        from appname.person import Person
        urlsafe = self.request.path.rsplit('/', 1)[-1]
        if not urlsafe:
            return

        key = ndb.Key(urlsafe=urlsafe)
        if key.kind() != Person._get_kind():
            self.error(500)
            return

        key.delete()
        logging.info("Deleted person with key: %s", urlsafe)

    def post(self):
        self.process()

    def put(self):
        self.process()

    def process(self):
        from voluptuous import Schema
        from appname.person import Person
        from appname.person import person_schema

        person = json.loads(self.request.body)
        schema = Schema(person_schema, extra=True)
        try:
            schema(person)
        except:
            logging.exception('validation failed')
            logging.info(person)

        person_entity = Person.from_dict(person)
        person_entity.put()

        out = person_entity.to_dict()
        self.response.out.write(json.dumps(out))


class VendorHandler(webapp2.RequestHandler):
    def get(self):
        from appname.vendor import Vendor
        user_query = self.request.get('query')
        limit = int(self.request.get('limit', 40))

        query = Vendor.query()
        if user_query:
            search = user_query.strip().lower()
            query = query.filter(Vendor.n_ >= search)
            query = query.filter(Vendor.n_ < search + u"\uFFFD")

        if limit > 0:
            query = query.fetch(limit)

        out = [entity.to_dict() for entity in query]
        self.response.out.write(json.dumps(out))

    def delete(self):
        from google.appengine.ext import ndb
        from appname.vendor import Vendor
        urlsafe = self.request.path.rsplit('/', 1)[-1]
        if not urlsafe:
            return

        key = ndb.Key(urlsafe=urlsafe)
        if key.kind() != Vendor._get_kind():
            self.error(500)
            return

        key.delete()
        logging.info("Deleted vendor with key: %s", urlsafe)

    def post(self):
        self.process()

    def put(self):
        self.process()

    def process(self):
        from voluptuous import Schema
        from appname.vendor import Vendor
        from appname.vendor import vendor_schema

        vendor = json.loads(self.request.body)
        schema = Schema(vendor_schema, extra=True)
        try:
            schema(vendor)
        except:
            logging.exception('validation failed')
            logging.info(vendor)

        vendor_entity = Vendor.from_dict(vendor)
        vendor_entity.put()

        user_id = users.get_current_user().user_id()
        person = Person.get_by_id(user_id)
        if vendor_entity.is_new:
            what = "Vendor Created."
        else:
            what = "Vendor Updated."
        what = "%s %s with tags: %s" % (what, vendor_entity.name, vendor_entity.tags)
        loc = ""
        if person is not None and person.location_info is not None:
            loc = person.location_info.get('latlong')
        message = {'location': loc,
                    'what': what}
        event.send("ACTIVITY", message)
        logging.info("Sending message: %s" % message)


        out = vendor_entity.to_dict()
        self.response.out.write(json.dumps(out))


class TransactionHandler(webapp2.RequestHandler):
    def get(self):
        from appname.transaction import Transaction
        limit = int(self.request.get('limit', 40))

        query = Transaction.query()

        if limit > 0:
            query = query.fetch(limit)

        out = [entity.to_dict() for entity in query]
        self.response.out.write(json.dumps(out))

    def delete(self):
        from google.appengine.ext import ndb
        from appname.transaction import Transaction
        urlsafe = self.request.path.rsplit('/', 1)[-1]
        if not urlsafe:
            return

        key = ndb.Key(urlsafe=urlsafe)
        if key.kind() != Transaction._get_kind():
            self.error(500)
            return

        key.delete()
        logging.info("Deleted transaction with key: %s", urlsafe)

    def post(self):
        self.process()

    def put(self):
        self.process()

    def process(self):
        from voluptuous import Schema
        from appname.transaction import Transaction
        from appname.transaction import transaction_schema

        transaction = json.loads(self.request.body)
        schema = Schema(transaction_schema, extra=True)
        try:
            schema(transaction)
        except:
            logging.exception('validation failed')
            logging.info(transaction)

        transaction_entity = Transaction.from_dict(transaction)
        transaction_entity.put()

        user_id = users.get_current_user().user_id()
        person = Person.get_by_id(user_id)
        if transaction_entity.is_new:
            what = "Transaction Created."
        else:
            what = "Transaction Updated."
        what = "%s $%s at %s" % (what, transaction_entity.amount, transaction_entity.vendor_name)
        loc = ""
        if person is not None and person.location_info is not None:
            loc = person.location_info.get('latlong')
        message = {'location': loc,
                    'what': what}
        event.send("ACTIVITY", message)
        logging.info("Sending message: %s" % message)

        out = transaction_entity.to_dict()
        self.response.out.write(json.dumps(out))

class TransactionSpreadsheetHandler(webapp2.RequestHandler):
    def get(self):
        from appname.transaction import Transaction, get_transactions_from_google_spreadsheet
        import datetime
        data = get_transactions_from_google_spreadsheet()
        logging.info(data)
        for d in data:
            Transaction(date=datetime.datetime.strptime(d[0], '%d/%m/%Y'), vendor_name=d[1], amount=d[2]).put()

class ChannelTokenHandler(webapp2.RequestHandler):

    def get(self):
        from google.appengine.api import channel

        from uuid import uuid4

        user_id = users.get_current_user().user_id()

        channel_id = user_id + uuid4().hex

        token = channel.create_channel(channel_id)

        # We will send Activity to everyone
        event.subscribe("ACTIVITY", channel_id)
        # We will send results from aggregations just to the
        # user who created the data.
        event.subscribe("SUMMARY-%s" % user_id, channel_id)

        self.response.out.write(json.dumps({
                "token": token
            }))


class SummaryHandler(webapp2.RequestHandler):
    """The summary endpoint only supports read operations,
    modification of the stats entities happens only through
    the well-defined aggregation process.
    """

    def get(self):
        from appname.aggregators import TagStats
        tag = self.request.get('tag')
        period = self.request.get('period')
        limit = int(self.request.get('limit', 10))

        query = TagStats.query()
        if tag:
            search_tag = tag.strip().lower()
            query = query.filter(TagStats.tag == search_tag)

        # Default to finding days.
        if not period:
            period = 'd'
        query = query.filter(TagStats.period_type == period)

        # Cap the maximum at 1000
        if 0 < limit < 1000:
            stats = query.fetch(limit)
        else:
            stats = query.fetch(1000)

        out = [entity.to_dict() for entity in stats]
        self.response.out.write(json.dumps(out))



class ChannelConnectedHandler(webapp2.RequestHandler):
    """
    Called when a Channel has been connected.
    """


    def post(self):
        import event

        channel_id = self.request.get('from')

        event.subscribe('ACTIVITY', channel_id)
        event.subscribe('SUMMARY-%s' % channel_id, channel_id)



class ChannelDisconnectedHandler(webapp2.RequestHandler):
    """
    Called when a Channel has been disconnected.
    """


    def post(self):
        import event

        channel_id = self.request.get('from')

        event.unsubscribe('ACTIVITY', channel_id)
        event.unsubscribe('SUMMARY-%s' % channel_id, channel_id)
