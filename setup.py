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

from setuptools import setup, find_packages

version = '1.0.4'

setup(
    name='snmposter',
    version=version,
    description="SNMP Agent Simulator",
    long_description="""
""",

    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        ],

    keywords='snmp agent simulator snmpwalk',
    author='Chet Luther',
    author_email='chet.luther@gmail.com',
    url='http://github.com/cluther/snmposter',
    license='Apache 2',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'Twisted==22.4.0',
        #'TwistedSNMP', Not currently installable via PyPI.
        #'pysnmp-se', Not currently installable via PyPI.
        ],

    entry_points={
        'console_scripts': [
            'snmposter = snmposter.scripts:launcher',
            ]
        },
    )
