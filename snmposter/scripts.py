# Copyright 2010 Chet Luther <chet.luther@gmail.com>
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

import sys
from optparse import OptionParser
from snmposter import SNMPosterFactory


def launcher():
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename',
            default='agents.csv',
            help='snmposter configuration file')
    options, args = parser.parse_args()

    factory = SNMPosterFactory()

    try:
        factory.configure(options.filename)
    except IOError:
        print >> sys.stderr, "Error opening %s." % options.filename
        sys.exit(1)

    factory.start()
