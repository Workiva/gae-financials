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

"""Logic to handle batching and applying of updates to our tag stats."""

import json
from decimal import Decimal

from google.appengine.ext import ndb
from google.appengine.api import taskqueue

import webapp2


class TagStats(ndb.Model):
    """Stats about Tag entities."""
    period = ndb.StringProperty('p')
    period_length = ndb.ComputedProperty(lambda self: len(self.period), name='pl')

    tag = ndb.StringProperty('t')

    stats = ndb.JsonProperty('s')
    index = ndb.JsonProperty('i')


class WorkBatcherHandler(webapp2.RequestHandler):
    def post(self):
        """Bundle up work and apply it to our TagStats entity."""
        queue = taskqueue.Queue('work-queue')
        work = queue.lease_tasks_by_tag(30, 500)
        apply_work(work)
        queue.delete_tasks(work)


@ndb.transactional
def apply_work(work):
    """Apply the work units to the TagStats entity.

    Note: all work must belong to the same aggregation set.
    """
    if not work:
        return

    tag = work[0].tag

    stat_model_keys, payloads = _parse_work_tasks(work)

    root_stat_key = stat_model_keys[0]

    stat_models = dict(
        (key, model) for key, model in zip(stat_model_keys,
                                           ndb.get_multi(stat_model_keys)))

    for unit in payloads:
        amount = Decimal(unit['amount'])

        for model_key in [root_stat_key, unit['stat_key']]:
            stat_model = stat_models.get(model_key)
            if not stat_model:
                stat_model = TagStats(
                    key=model_key,
                    tag=tag,
                    period=unit['date'])
                stat_models[model_key] = stat_model

            stats = model.stats
            if not stats:
                stats = model.stats = {
                    'n': 0,
                    's': Decimal('0.00'),
                }

            stats['n'] += 1
            stats['s'] = str(Decimal(stats['s']) + amount)

    ndb.put_multi(stat_models.values())


def _parse_work_tasks(work):
    """Parse the work tasks and return stat_model_keys and payloads."""
    tag = work[0].tag
    root_stat_key = ndb.Key(TagStats, tag)

    stat_model_keys = set((root_stat_key,))
    payloads = []
    for unit in work:
        payload = json.loads(unit.payload)
        payloads.append(payload)

        stat_key = ndb.Key(TagStats, payload['date'], parent=root_stat_key)
        stat_model_keys.add(stat_key)
        payload['stat_key'] = stat_key

    return list(stat_model_keys), payloads

