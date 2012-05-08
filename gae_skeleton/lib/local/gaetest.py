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

"""Simple TestCase which handles setup and defines methods that are often
useful when unit testing App Engine Applications.
"""


import unittest
from unittest import *

from google.appengine.ext import db
from google.appengine.ext import testbed


class TestCase(unittest.TestCase, testbed.Testbed):
    """
    GAE Specific asserts.
    """
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        testbed.Testbed.__init__(self)

    def setUp(self):
        super(TestCase, self).setUp()
        self.activate()

    def tearDown(self):
        self.deactivate()
        super(TestCase, self).tearDown()

    def patch(self, obj, attr, value):
        """
        Monkey patch an object for the duration of the test.

        The monkey patch will be reverted at the end of the test using the
        L{addCleanup} mechanism.

        @param obj: The object to monkey patch.
        @param attr: The name of the attribute to change.
        @param value: The value to set the attribute to.
        """
        sentinel = object()
        old = getattr(obj, attr, sentinel)

        def restore():
            if old is sentinel:
                delattr(obj, attr)
            else:
                setattr(obj, attr, old)

        self.addCleanup(restore)

        setattr(obj, attr, value)

    def patch_via(self, obj, attr):
        """
        Same as L{patch} but in a decorator
        """
        def decorator(fn):
            self.patch(obj, attr, fn)

            return fn

        return decorator

    def assertSameEntity(self, first, second, msg=None):
        """
        Fail the test if C{first} and C{second} are not considered the same entity
        within the datastore.
        """
        if hasattr(first, 'key'):
            try:
                first = first.key()
            except db.NotSavedError:
                raise AssertionError('%r is not persisted' % (first,))

            if hasattr(second, 'key'):
                try:
                    second = second.key()
                except db.NotSavedError:
                    raise AssertionError('%r is not persisted' % (second,))

            res = first == second

            if not res:
                raise AssertionError(msg or '%r != %r' % (first, second))

    def assertNotSameEntity(self, first, second, msg=None):
        """
        Fail the test if C{first} and C{second} C{ARE} considered the same entity
        within the datastore.
        """
        try:
            self.assertSameEntity(first, second, 'foo')
        except AssertionError, e:
            if str(e) != 'foo':
                raise
            else:
                raise AssertionError(msg or '%r = %r' % (first, second))

