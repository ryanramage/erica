# -*- coding: utf-8 -*-
#
# This file is part of couchapp released under the Apache 2 license. 
# See the NOTICE for more information.

import os
import sys

if not hasattr(sys, 'version_info') or sys.version_info < (2, 5, 0, 'final'):
    raise SystemExit("Couchapp requires Python 2.5 or later.")

try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    
extra = {}
data_files = []

for dir, dirs, files in os.walk('templates'):
    data_files.append((os.path.join('couchapp', dir), 
        [os.path.join(dir, file_) for file_ in files]))

for dir, dirs, files in os.walk('vendor'):
    data_files.append((os.path.join('couchapp', dir), 
        [os.path.join(dir, file_) for file_ in files]))
    
packages = ['couchapp', 'couchapp.simplejson', 'couchappext', 
          'couchappext.compress',]


# py2exe needs to be installed to work
try:
    import py2exe

    # Help py2exe to find win32com.shell
    try:
        import modulefinder
        import win32com
        for p in win32com.__path__[1:]: # Take the path to win32comext
            modulefinder.AddPackagePath("win32com", p)
        pn = "win32com.shell"
        __import__(pn)
        m = sys.modules[pn]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(pn, p)
    except ImportError:
        pass
    
except ImportError:
    pass
    
from couchapp import __version__ as version
 
setup(
    name = 'Couchapp',
    version = version,
    url = 'http://github.com/couchapp/couchapp/tree/master',
    license =  'Apache License 2',
    author = 'Benoit Chesneau',
    author_email = 'benoitc@e-engura.org',
    description = 'Standalone CouchDB Application Development Made Simple.',
    long_description = """CouchApp is a set of helpers and a jQuery plugin
    that conspire to get you up and running on CouchDB quickly and
    correctly. It brings clarity and order to the freedom of CouchDB's
    document-based approach.""",
    keywords = 'couchdb couchapp',
    platforms = ['any'],
    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Utilities',
    ],

    packages= find_packages(exclude=['tests']),
    data_files = data_files,
    include_package_data = True,
    
    install_requires = [],
    options = dict(py2exe=dict(packages=['couchappext']),
                   bdist_mpkg=dict(zipdist=True,
                                   license='LICENSE',
                                   readme='contrib/macosx/Readme.html',
                                   welcome='contrib/macosx/Welcome.html')),
                                   
    entry_points="""
    [console_scripts]
    couchapp=couchapp.dispatch:run
    """,
    test_suite='tests',
    **extra
)
