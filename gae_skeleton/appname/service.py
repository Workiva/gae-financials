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

import webapp2


class PersonHandler(webapp2.RequestHandler):
    def get(self):
        from appname.person import Person
        user_query = self.request.get('query')
        limit = int(self.request.get('limit', 10))

        query = Person.query()
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
        if key.kind != Person._get_kind():
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
        limit = int(self.request.get('limit', 10))

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
        if key.kind != Vendor._get_kind():
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

        out = vendor_entity.to_dict()
        self.response.out.write(json.dumps(out))


class TransactionHandler(webapp2.RequestHandler):
    def get(self):
        from appname.transaction import Transaction
        limit = int(self.request.get('limit', 10))

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
        if key.kind != Transaction._get_kind():
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

        out = transaction_entity.to_dict()
        self.response.out.write(json.dumps(out))

