## snmposter
SNMP Agent Simulator

This tool allows you to take the output of an snmpwalk command and then pretend
to be the agent that it was gathered from. This can be useful when you're
developing SNMP management tools.

### Requirements
Twisted, TwistedSNMP and PySNMP-SE.

Twisted is available from PyPI and will be automatically installed if you go
the route of easy_install or pip. TwistedSNMP and PySNMP-SE are not currently
available from PyPI and should be individually downloaded from sourceforge
and installed from source.

### Installation
First you must download and install the dependencies. If you have Internet
access the easiest way to do this is by running the following commands.

Install TwistedSNMP Dependency

    wget http://downloads.sourceforge.net/project/twistedsnmp/twistedsnmp/0.3.13/TwistedSNMP-0.3.13.tar.gz
    tar -xzf TwistedSNMP-0.3.13.tar.gz
    cd TwistedSNMP-0.3.13
    python setup.py install
    cd ..

Install PySNMP-SE Dependency

    wget http://downloads.sourceforge.net/project/twistedsnmp/pysnmp-se/3.5.2/pysnmp-se-3.5.2.tar.gz
    tar -xzf pysnmp-se-3.5.2.tar.gz
    cd pysnmp-se-3.5.2
    python setup.py install
    cd ..

Install snmposter

    easy_install snmposter

### Usage
Installing will create a command line tool called `snmposter`. This tool
requires root access because it listens on 161/udp and creates loopback aliases
to support emulating multiple SNMP agents simultaneously.

The `snmposter` command takes a single command line argument: -f or --file.
The file passed to this option must contain one or more rows with two columns
each. The first column should be the absolute or relative path to a file
containing the output of an snmpwalk command. The second column should contain
an IP address that this snmpwalk data will be exposed on.

Example usage:

    sudo snmposter /etc/snmposter/agents.csv

Example contents of `/etc/snmposter/agents.csv`:

    /etc/snmposter/agents/Cisco_2811.snmpwalk,127.0.1.11
    /etc/snmposter/agents/NetApp_Filer_FAS3020.snmpwalk,127.0.1.12

This example usage will cause snmposter to run in the background, create two
new IP aliases on the loopback interface (127.0.1.11 and 127.0.1.12), and
expose the contents of each snmpwalk file as an SNMP agent on UDP port 161 of
the appropriate IP address. If you're going to be using this frequently I
would recommend adding some entries to your `/etc/hosts` file to make it even
easier.

Example additions to `/etc/hosts`:

    127.0.1.11      cisco-2811
    127.0.1.12      netapp-filer-fa3020


**Important Note**: The snmpwalk output file that snmposter consumes must be
generated with very specific snmpwalk command line options. These options allow
snmposter to get the most raw data possible and provides the most accurate
simulation.

Example snmpwalk command to generate the above `Cisco_2811.snmpwalk` file:

    snmpwalk -v2c -c public -m none -O enU 10.120.5.1 > Cisco_2811.snmpwalk
    snmpwalk -v2c -c public -m none -O enU 10.120.5.1 .1.3.6.1.4.1.9 >> Cisco_2811.snmpwalk

The important command line options are `-m none -O enU` to get the raw output.
Don't worry if you get an error like `Cannot find module (none): At line 0 in
(none)` as this is expected and a result of us trying to load a non-existent
MIB.

It's also important to note that this example shows running two snmpwalk
commands with the second one appending to the .snmpwalk file. The reason this
is necessary is that most (all?) SNMP agents will only respond with the MIB-2
tree with the non-specific walk requested by the first command. You then have
to walk the enterprise MIB separately to get that data. The enterprise MIB
differs from vendor to vendor. `.1.3.6.1.4.1.9` is an example that works for
Cisco devices.
