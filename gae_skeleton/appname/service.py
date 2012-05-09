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

