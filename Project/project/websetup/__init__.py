# -*- coding: utf-8 -*-
"""Setup the Project application"""

import logging
from project.config.environment import load_environment
from .schema import setup_schema
from .bootstrap import bootstrap


__all__ = ['setup_app']

log = logging.getLogger(__name__)


def setup_app(command, conf, vars):
    """Place any commands to setup project here"""
    load_environment(conf.global_conf, conf.local_conf)
    setup_schema(command, conf, vars)
    bootstrap(command, conf, vars)
