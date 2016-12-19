# -*- coding: utf-8 -*-

# This is just a work-around for a Python2.7 issue causing
# interpreter crash at exit when trying to log an info message.
try:
    import logging
    import multiprocessing
except:
    pass

import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs = [
    'WebTest >= 1.2.3',
    'nose',
    'coverage',
    'gearbox'
]

install_requires = [
    "TurboGears2 >= 2.3.9",
    "Beaker >= 1.8.0",
    "Kajiki >= 0.3.5",
    "ming>=0.4.3",
    "repoze.who",
    "tw2.forms",
    "tgext.admin >= 0.6.1",
    "WebHelpers2",
    "ez_setup"
]

if py_version != (3, 2):
    # Babel not available on 3.2
    install_requires.append("Babel")

setup(
    name='Project',
    version='0.1',
    description='',
    author='Chirukhin Aleksey',
    author_email='pr3sto1377@gmail.com',
    url='',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'project': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'project': [
        ('**.py', 'python', None),
        ('templates/**.xhtml', 'kajiki', None),
        ('public/**', 'ignore', None)
    ]},
    entry_points={
        'paste.app_factory': [
            'main = project.config.middleware:make_app'
        ],
        'gearbox.plugins': [
            'turbogears-devtools = tg.devtools'
        ]
    },
    zip_safe=False
)
