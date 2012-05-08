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

"""Person model definition and business logic."""

from google.appengine.ext import ndb

person_schema = {
    'key': basestring,
    'name': basestring,
    'notes': basestring,
    'contact_info': [{'type': basestring, 'value': basestring}],
}

class Person(ndb.Model):
    """Represents a person."""
    # Store the schema version, to aid in migrations.
    version_ = ndb.IntegerProperty('v_', default=1)

    # The entity's change revision counter.
    revision = ndb.IntegerProperty('r_', default=0)

    # Useful timestamps.
    added = ndb.DateTimeProperty('a_', auto_now_add=True)
    modified = ndb.DateTimeProperty('m_', auto_now=True)

    # Person code, name, key
    name = ndb.StringProperty('n', indexed=False)
    n_ = ndb.ComputedProperty(lambda self: self.name.lower())

    # Phone / email / whatever.
    contact_info = ndb.JsonProperty('ci')

    # General remarks.
    notes = ndb.TextProperty('no')

    def _pre_put_hook(self):
        """Ran before the entity is written to the datastore."""
        self.revision += 1

    @classmethod
    def from_dict(cls, data):
        """Instantiate a Person entity from a dict of values."""
        key = data.get('key')
        person = None
        if key:
            key = ndb.Key(urlsafe=key)
            person = key.get()

        if not person:
            person = cls()

        person.name = data.get('name')
        person.contact_info = data.get('contact_info')
        person.notes = data.get('notes')

        return person

    def to_dict(self):
        """Return a Person entity represented as a dict of values
        suitable for rebuilding via Person.from_dict.
        """
        person = {
            'version': self.version_,
            'key': self.key.urlsafe(),
            'revision': self.revision,
            'added': self.added.strftime('%Y-%m-%d %h:%M'),
            'modified': self.modified.strftime('%Y-%m-%d %h:%M'),

            # name
            'name': self.name,

            # Contact info
            'contact_info': self.contact_info,

            # Notes
            'notes': self.notes,
        }
        return person

