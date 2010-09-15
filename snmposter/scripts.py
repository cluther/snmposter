##############################################################################
#
# Copyright (C) 2010, Chet Luther <chet.luther@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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
