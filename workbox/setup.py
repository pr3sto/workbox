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
    "Kajiki >= 0.6.1",
    "ming >= 0.4.3",
    "repoze.who",
    "tw2.forms",
    "gearbox",
    "tgext.admin >= 0.6.1",
    "WebHelpers2",
    "markupsafe >= 1.0",
    "python-vagrant >= 0.5.14",
    "psutil >= 5.2.2"
]

if py_version != (3, 2):
    # Babel not available on 3.2
    install_requires.append("Babel")

setup(
    name='workbox',
    version='1.0',
    description='Service for maintaining virtual environments',
    maintainer='Alexey Chirukhin',
    maintainer_email='pr3sto1377@gmail.com',
    author='Alexey Chirukhin',
    author_email='pr3sto1377@gmail.com',
    url='',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'workbox': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'workbox': [
        ('**.py', 'python', None),
        ('templates/**.xhtml', 'kajiki', {'strip_text': False}),
        ('public/**', 'ignore', None)
    ]},
    entry_points={
        'paste.app_factory': [
            'main = workbox.config.middleware:make_app'
        ],
        'gearbox.plugins': [
            'turbogears-devtools = tg.devtools'
        ]
    },
    zip_safe=False
)
