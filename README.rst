=============================================================================
snmposter
=============================================================================

SNMP Agent Simulator

This tool allows you to take the output of an snmpwalk command and then pretend
to be the agent that it was gathered from. This can be useful when you're
developing SNMP management tools.

Requirements
=============================================================================

Twisted, TwistedSNMP and PySNMP-SE.

Twisted is available from PyPI and will be automatically installed if you go
the route of easy_install or pip. TwistedSNMP and PySNMP-SE are not currently
available from PyPI and should be individually downloaded from sourceforge
and installed from source.

Installation
=============================================================================

I recommend installing *snmposter* within a Python virtualenv. This makes it
easier to install on operating systems such as CentOS 5 where the default
system Python version is older than 2.5. Due to the dependency on *Twisted*,
snmposter requires Python 2.5 or newer.

Red Hat Enterprise Linux or CentOS 6
-----------------------------------------------------------------------------

The following steps are specific to Red Hat Enterprise Linux 6 or one of its
compatible distributions such as CentOS.

1. Install Python development tools.

   .. sourcecode:: bash

      yum -y install python-devel gcc

2. Install, setup and activate virtualenv.

   .. sourcecode:: bash

      yum -y install python-virtualenv
      virtualenv /snmposter
      source /snmposter/bin/activate

3. Install TwistedSNMP dependency.

   .. sourcecode:: bash

      wget http://downloads.sourceforge.net/project/twistedsnmp/twistedsnmp/0.3.13/TwistedSNMP-0.3.13.tar.gz
      tar -xzf TwistedSNMP-0.3.13.tar.gz
      cd TwistedSNMP-0.3.13
      python setup.py install
      cd ..

4. Install PySNMP-SE dependency.

   .. sourcecode:: bash

      wget http://downloads.sourceforge.net/project/twistedsnmp/pysnmp-se/3.5.2/pysnmp-se-3.5.2.tar.gz
      tar -xzf pysnmp-se-3.5.2.tar.gz
      cd pysnmp-se-3.5.2
      python setup.py install
      cd ..

5. Install snmposter.

   .. sourcecode:: bash

      pip install snmposter


Red Hat Enterprise Linux or CentOS 5
-----------------------------------------------------------------------------

The following steps are specific to Red Hat Enterprise Linux 5 or one of its
compatible distributions such as CentOS.

1. Install the EPEL repository.

   .. sourcecode:: bash

      rpm -ivh http://mirror.cogentco.com/pub/linux/epel/5/i386/epel-release-5-4.noarch.rpm

2. Install Python 2.6 and development tools.

   .. sourcecode:: bash

      yum -y --enablerepo=epel install python26-devel gcc

2. Install, setup and activate virtualenv.

   .. sourcecode:: bash

      yum -y --enablerepo=epel install python26-virtualenv
      virtualenv-2.6 /snmposter
      source /snmposter/bin/activate

3. Install TwistedSNMP dependency.

   .. sourcecode:: bash

      wget http://downloads.sourceforge.net/project/twistedsnmp/twistedsnmp/0.3.13/TwistedSNMP-0.3.13.tar.gz
      tar -xzf TwistedSNMP-0.3.13.tar.gz
      cd TwistedSNMP-0.3.13
      python setup.py install
      cd ..

4. Install PySNMP-SE dependency.

   .. sourcecode:: bash

      wget http://downloads.sourceforge.net/project/twistedsnmp/pysnmp-se/3.5.2/pysnmp-se-3.5.2.tar.gz
      tar -xzf pysnmp-se-3.5.2.tar.gz
      cd pysnmp-se-3.5.2
      python setup.py install
      cd ..

5. Install snmposter.

   .. sourcecode:: bash

      pip install snmposter


Usage
=============================================================================

Installing will create a command line tool called `snmposter`. This tool
requires root access because it listens on 161/udp and creates loopback aliases
to support emulating multiple SNMP agents simultaneously.

The `snmposter` command takes a single command line argument: -f or --file.
The file passed to this option must contain one or more rows with two columns
each. The first column should be the absolute or relative path to a file
containing the output of an snmpwalk command. The second column should contain
an IP address that this snmpwalk data will be exposed on.

Example usage:

.. sourcecode:: bash

   source /snmposter/bin/activate
   snmposter -f /etc/snmposter/agents.csv

Example contents of `/etc/snmposter/agents.csv`::

    /etc/snmposter/agents/Cisco_2811.snmpwalk,127.0.1.11
    /etc/snmposter/agents/NetApp_Filer_FAS3020.snmpwalk,127.0.1.12

This example usage will cause snmposter to run in the background, create two
new IP aliases on the loopback interface (127.0.1.11 and 127.0.1.12), and
expose the contents of each snmpwalk file as an SNMP agent on UDP port 161 of
the appropriate IP address. If you're going to be using this frequently I
would recommend adding some entries to your `/etc/hosts` file to make it even
easier.

Example additions to `/etc/hosts`::

    127.0.1.11      cisco-2811
    127.0.1.12      netapp-filer-fa3020


**Important Note**: The snmpwalk output file that snmposter consumes must be
generated with very specific snmpwalk command line options. These options allow
snmposter to get the most raw data possible and provides the most accurate
simulation.

Example snmpwalk command to generate the above `Cisco_2811.snmpwalk` file:

.. sourcecode:: bash

   snmpwalk -v2c -c public -ObentU localhost .1 > Cisco_2811.snmpwalk

The important command line options are `-m none -O enU` to get the raw output and '-C c' 
to ignore out of sequence responses from the switch. (Sometimes this validation error is 
triggered when walking routing MIBS on some switches)

Don't worry if you get an error like `Cannot find module (none): At line 0 in
(none)` as this is expected and a result of us trying to load a non-existent
MIB.
