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

from twisted.internet import reactor
from twistedsnmp import agent, agentprotocol, bisectoidstore, datatypes
from twistedsnmp.pysnmpproto import v2c, rfc1902

import sys
import os
import re
import csv


# twistedsnmp has a bug that causes it to fail to properly convert Counter64
# values. We workaround this by retroactively fixing datatypes mappings.
fixed_v2Mapping = []
for datatype, converter in datatypes.v2Mapping:
    if datatype == v2c.Counter64:
        fixed_v2Mapping.append(
            (datatype, datatypes.SimpleConverter(v2c.Counter64)))
    else:
        fixed_v2Mapping.append((datatype, converter))

datatypes.v2Mapping = fixed_v2Mapping

fixed_v1Mapping = [(rfc1902.Counter64, datatypes.SimpleConverter(v2c.Counter64))]
for datatype, converter in datatypes.v1Mapping:
    if datatype != rfc1902.Counter64:
        fixed_v1Mapping.append((datatype, converter))

datatypes.v1Mapping = fixed_v1Mapping


def sanitize_dotted(string):
    """Return dotted decimal strings with non-numerics replaced with 1.

    This is necessary because some snmpwalk output files have had IP
    addresses obscured with non-numeric characters.

    """

    return re.sub(r'[^ \.\d]', '1', string)


class SNMPosterFactory:
    agents = []

    def configure(self, filename):
        reader = csv.reader(open(filename, "rb"))
        for row in reader:
            if row[0].startswith('#'):
                continue

            self.agents.append({
                'filename': row[0],
                'ip': row[1]})

    def start(self):
        for a in self.agents:
            print "Starting %s on %s." % (a['filename'], a['ip'])
            if os.uname()[0] == 'Darwin':
                os.popen("ifconfig lo0 alias %s up" % (a['ip'],))
            elif os.uname()[0] == 'Linux':
                os.popen("/sbin/ip addr add %s dev lo" % (a['ip'],))
            else:
                print "WARNING: Unable to add loopback alias on this platform."

            faker = SNMPoster(a['ip'], a['filename'])
            faker.run()

        daemonize()
        reactor.run()


class SNMPoster:
    oidData = {}
    sortedOids = []

    def __init__(self, ip, filename):
        self.ip = ip
        self.oids = {}

        oid = ''
        type = ''
        value = []

        file = open(filename, 'r')
        for line in file:
            line = line.rstrip()

            match = re.search(r'^([^ ]+) = ([^\:]+):\s*(.*)$', line)
            if not match:
                match = re.search(r'^([^ ]+) = (".*")$', line)

            if match:
                if len(value) > 0:
                    if type == 'Counter32':
                        self.oids[oid] = v2c.Counter32(self.tryIntConvert(value[0]))
                    elif type == 'Counter64':
                        self.oids[oid] = rfc1902.Counter64(long(value[0]))
                    elif type == 'Gauge32':
                        self.oids[oid] = v2c.Gauge32(self.tryIntConvert(value[0]))
                    elif type == 'Hex-STRING':
                        value = [sanitize_dotted(x) for x in value]
                        self.oids[oid] = ''.join(
                            [chr(int(c, 16)) \
                                for c in ' '.join(value).split(' ')])
                    elif type == 'INTEGER':
                        self.oids[oid] = self.tryIntConvert(value[0])
                    elif type == 'IpAddress':
                        value[0] = sanitize_dotted(value[0])
                        self.oids[oid] = v2c.IpAddress(value[0])
                    elif type == 'OID':
                        self.oids[oid] = v2c.ObjectIdentifier(value[0])
                    elif type == 'STRING':
                        self.oids[oid] = '\n'.join(value)
                    elif type == 'Timeticks':
                        self.oids[oid] = v2c.TimeTicks(int(value[0]))
                    oid = ''
                    type = ''
                    value = []

                groups = match.groups()
                if len(groups) == 3:
                    oid, type, value1 = groups
                else:
                    oid, type, value1 = (groups[0], 'STRING', groups[1])

                oid = sanitize_dotted(oid)

                if type == 'Timeticks':
                    value1 = re.search(r'^\((\d+)\) .*$', value1) \
                               .groups()[0]
                value.append(value1.strip('"'))
            else:
                value.append(line.strip('"'))

        file.close()

    def tryIntConvert(self, myint):
        conv = -1
        try:
            conv = int(myint)
        except:
            m = re.match(".*\((?P<myint>\d+)\).*|(?P<myint2>\d+).*", myint)
            if m:
                myint2 = m.groupdict()["myint"] or m.groupdict()["myint2"]
                try:
                    conv = int(myint2)
                except:
                    pass
        return conv

    def start(self):
        reactor.listenUDP(
            161, agentprotocol.AgentProtocol(
                snmpVersion='v2c',
                agent=agent.Agent(
                    dataStore=bisectoidstore.BisectOIDStore(
                        OIDs=self.oids,
                        ),
                    ),
                ),
                interface=self.ip,
            )

    def run(self):
        reactor.callWhenRunning(self.start)


def daemonize():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)
