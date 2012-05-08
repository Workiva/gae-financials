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


import os
import sys

from fabric.api import local

sys.path.append(os.path.join('lib', 'local', 'scripts'))


def dev():
    import assets
    assets.build(debug=True, cache=False)
    assets.watch(debug=True, cache=False)

def build():
    import assets
    assets.build(debug=False, cache=True)

def cleanpy():
    local('find . -name "*.pyc" -delete')

def test(args=''):
    path = os.path.join('lib', 'local', 'scripts', 'test.py')
    local('python %s %s' % (path, args))
    local('cd assets; mocha --compilers coffee:coffee-script')

def run(port='8080', address='localhost'):
    import runserver
    runserver.run(port, address)

