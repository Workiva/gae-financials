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

"""Transaction model definition and business logic."""

import base64
from google.appengine.ext import ndb
import logging

transaction_schema = {
    'key': basestring,
    'date': basestring,
    'vendor': basestring,
    'amount': basestring,
}

class Transaction(ndb.Model):
    """Represents a transaction."""
    # Store the schema version, to aid in migrations.
    version_ = ndb.IntegerProperty('v_', default=1)

    # The entity's change revision counter.
    revision = ndb.IntegerProperty('r_', default=0)

    # Useful timestamps.
    added = ndb.DateTimeProperty('a_', auto_now_add=True)
    modified = ndb.DateTimeProperty('m_', auto_now=True)

    # Transaction date
    date = ndb.DateTimeProperty('d', indexed=False)
    vendor_name = ndb.StringProperty('v', indexed=False)
    amount = ndb.StringProperty('a', indexed=False)
    #v_ = ndb.ComputedProperty(lambda self: self.vendor.lower())

    # List of tags
    tags = ndb.JsonProperty('t', indexed=False)

    def _pre_put_hook(self):
        """Ran before the entity is written to the datastore."""
        self.revision += 1

    def _post_put_hook(self, tasklet_future):
        """Ran after the entity is written to the datastore."""
        import json
        from google.appengine.api import taskqueue
        from google.appengine.api import namespace_manager

        if not self.tags:
            return

        # TODO:  Note that deletions and changes of day will result in
        # over counting.  A reversing entry needs made for those items.
        work = []
        for tag_data in self.tags:
            tag = tag_data['name'].lower()
            task_name = "%s_%s_%s" % (tag, self.key.urlsafe(), self.revision)
            work.append(taskqueue.Task(
                method='PULL',
                name=task_name,
                tag=tag,
                payload=json.dumps({
                    'entity': self.key.urlsafe(),
                    'rev': self.revision,
                    'date': self.date.strftime('%Y%m%d%H%M'),
                    'amount': self.amount,
                    'namespace': namespace_manager.get_namespace()
                }),
            ))
        taskqueue.Queue(name='work-groups').add(work)
        taskqueue.add(
            queue_name='default',
            url='/_ah/task/batcher'
        )

    @classmethod
    def normalize_date_input(cls, input):
        from time import mktime
        from datetime import datetime
        import parsedatetime.parsedatetime as pdt

        c = pdt.Calendar()
        result, what = c.parse(input)

        dt = None

        # what was returned (see http://code-bear.com/code/parsedatetime/docs/)
        # 0 = failed to parse
        # 1 = date (with current time, as a struct_time)
        # 2 = time (with current date, as a struct_time)
        # 3 = datetime
        if what in (1,2,3):
            # result is struct_time
            dt = datetime(*result[:6])

        if dt is None:
            try:
                dt = c.parseDate(input)
            except ValueError:
                dt = None

        return dt



    @classmethod
    def from_dict(cls, data):
        """Instantiate a Transaction entity from a dict of values."""
        from appname.vendor import Vendor

        key = data.get('key')
        transaction = None
        if key:
            key = ndb.Key(urlsafe=key)
            transaction = key.get()

        if not transaction:
            transaction = cls()
            transaction.is_new = True
        else:
            transaction.is_new = False

        transaction.date = cls.normalize_date_input(data.get('date'))
        transaction.vendor_name = data.get('vendor')

        # TODO: Use Python Decimal here with prec set to .00.
        transaction.amount = data.get('amount')

        vendor_keyname = base64.b64encode(transaction.vendor_name)
        vendor = Vendor.get_by_id(vendor_keyname)
        if vendor:
            transaction.tags = vendor.tags

        return transaction

    def to_dict(self):
        """Return a Transaction entity represented as a dict of values
        suitable for rebuilding via Transaction.from_dict.
        """
        transaction = {
            'version': self.version_,
            'key': self.key.urlsafe(),
            'revision': self.revision,
            'added': self.added.strftime('%Y-%m-%d %h:%M'),
            'modified': self.modified.strftime('%Y-%m-%d %h:%M'),

            # date
            'date': self.date.strftime('%m/%d/%Y %H:%M') if self.date is not None else "Bad Date",

            # vendor
            'vendor': self.vendor_name,

            # amount
            'amount': self.amount,
        }
        return transaction

def get_transactions_from_google_spreadsheet():
    import gdata.spreadsheet.service
    client = gdata.spreadsheet.service.SpreadsheetsService()
    key = '0Ahivi2ybuZeydGRjakJzeWFSMTJyb0t4UnFqVlRuNXc'
    rows = client.GetListFeed(key, visibility='public', projection='basic').entry
    ret = []
    for row in rows:
        # FIXME: do not put ',' or ':' in the spreadsheet
        cols = [cell.strip().split(': ')[1] for cell in row.content.text.split(', ')]
        ret.append(cols)
    return ret
