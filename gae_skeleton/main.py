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

"""Map user-facing handlers here.  This is meant to map actual HTML pages."""

import os
import sys
import logging

# Add lib to path.
libs_dir = os.path.join(os.path.dirname(__file__), 'lib')
if libs_dir not in sys.path:
    logging.debug('Adding lib to path.')
    sys.path.insert(0, libs_dir)

import webapp2

from mako import exceptions
from mako.template import Template

class Main(webapp2.RequestHandler):
    def get(self):
        try:
            template = Template(filename='templates/base.mako')
            out = template.render()
        except:
            out = exceptions.html_error_template().render()
            logging.exception('Oh NO! Rendering error.')

        self.response.out.write(out)

url_map = [('/', Main)]
app = webapp2.WSGIApplication(url_map)

