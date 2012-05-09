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

"""Setup paths and run App Engine's dev_appserver.py."""

import os
import sys

import argparse

CURRENT_PATH = os.getcwdu()

paths = [
    os.path.join(CURRENT_PATH, 'lib'),
    os.path.join(CURRENT_PATH, 'lib', 'local'),
]

from dev_appserver import fix_sys_path
fix_sys_path()

sys.path.extend(paths)


def run():
    parser = argparse.ArgumentParser(description='Run tests')
    parser.add_argument(
        '--port', '-p', type=int, default=8001)
    parser.add_argument('--address', '-a', default='localhost')

    args = parser.parse_args()

    start(args.port, args.address)


def start(port, address):
    """
    Starts the appengine dev_appserver program.

    Here dev_appserver.py is run with a set of default parameters. To pass
    special parameters, run dev_appserver.py manually.
    """
    from google.appengine.tools import dev_appserver_main

    args = [
        '--address', address,
        '--port', port,
        '--require_indexes',
        '--skip_sdk_update_check',
        '--high_replication',
        '--default_partition=',
        '--datastore_path=.appname.ds',
        '--allow_skipped_files',
        '--debug',
        #'--backends',
    ]

    # Append the current working directory to the arguments.
    run_args = [None]
    run_args.extend(args)
    run_args.append(CURRENT_PATH)

    sys.modules['__main__'] = dev_appserver_main
    #hack __main__ so --help in dev_appserver_main works OK.

    dev_appserver_main.main(run_args)


if __name__ == '__main__':
    run()
