#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import codecs
import os
import re
import sys


# When creating the sdist, make sure the django.mo file also exists:
if 'sdist' in sys.argv or 'develop' in sys.argv:
    os.chdir('fluentcms_contactform')
    try:
        from django.core.management.commands.compilemessages import Command
        command = Command()
        command.execute(stdout=sys.stderr, verbosity=1)
    except ImportError:
        # < Django 1.7
        try:
            from django.core.management.commands.compilemessages import compile_messages
            compile_messages(sys.stderr)
        except ImportError:
            pass
    finally:
        os.chdir('..')


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name='fluentcms-contactform',
    version=find_version('fluentcms_contactform', '__init__.py'),
    license='Apache 2.0',

    install_requires=[
        'django-fluent-contents>=1.0',
        'django-ipware>=1.1.1',
        'django-phonenumber-field>=0.7.2',
        'django-crispy-forms >= 1.3',
    ],
    requires=[
        'Django (>=1.4)',
    ],

    description='A contact form plugin django-fluent-contents',
    long_description=read('README.rst'),

    author='Diederik van der Boor',
    author_email='opensource@edoburu.nl',

    url='https://github.com/edoburu/fluentcms-contactform',
    download_url='https://github.com/edoburu/fluentcms-contactform/zipball/master',

    packages=find_packages(exclude=('example*',)),
    include_package_data=True,

    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)