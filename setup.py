# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

setup(
    name='django-sms',
    version='0.9.0',
    description='Sms queue with smsapi.pl gateway support for Django',
    author='Adam Bogdal',
    author_email='adam@bogdal.pl',
    url = 'https://github.com/bogdal/django-sms',
    download_url='',
    packages=find_packages(),
    package_data = {
        'sms': ['locale/*/LC_MESSAGES/*']
    },
    include_package_data=True,
    classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities'
    ],
    zip_safe = False,
    install_requires=[
        'suds',
    ],
)
