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

"""Vendor model definition and business logic."""

from google.appengine.ext import ndb

vendor_schema = {
    'key': basestring,
    'name': basestring,
    'notes': basestring,
    'tags': [{'name': basestring},],
}

class Vendor(ndb.Model):
    """Represents a vendor."""
    # Store the schema version, to aid in migrations.
    version_ = ndb.IntegerProperty('v_', default=1)

    # The entity's change revision counter.
    revision = ndb.IntegerProperty('r_', default=0)

    # Useful timestamps.
    added = ndb.DateTimeProperty('a_', auto_now_add=True)
    modified = ndb.DateTimeProperty('m_', auto_now=True)

    # Vendor name, key
    name = ndb.StringProperty('n', indexed=False)
    n_ = ndb.ComputedProperty(lambda self: self.name.lower())

    # List of tags
    tags = ndb.JsonProperty('t')

    # General remarks.
    notes = ndb.TextProperty('no')

    def _pre_put_hook(self):
        """Ran before the entity is written to the datastore."""
        self.revision += 1

    @classmethod
    def from_dict(cls, data):
        """Instantiate a Vendor entity from a dict of values."""
        import base64
        key = data.get('key')
        vendor = None
        if key:
            key = ndb.Key(urlsafe=key)
            vendor = key.get()

        if not vendor:
            vendor_keyname = base64.b64encode(data.get('name'))
            vendor_key = ndb.Key(cls, vendor_keyname)
            vendor = cls(key=vendor_key)

        vendor.name = data.get('name')
        vendor.tags = data.get('tags')
        vendor.notes = data.get('notes')

        return vendor

    def to_dict(self):
        """Return a Vendor entity represented as a dict of values
        suitable for rebuilding via Vendor.from_dict.
        """
        vendor = {
            'version': self.version_,
            'key': self.key.urlsafe(),
            'revision': self.revision,
            'added': self.added.strftime('%Y-%m-%d %h:%M'),
            'modified': self.modified.strftime('%Y-%m-%d %h:%M'),

            # name
            'name': self.name,

            # tags
            'tags': self.tags,

            # Notes
            'notes': self.notes,
        }
        return vendor

