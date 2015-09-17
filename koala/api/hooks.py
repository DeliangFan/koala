#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# filename   : hooks.py
# created at : 2013-07-01 21:05:45

from oslo.config import cfg
from pecan import hooks

from koala.db import api as dbapi


class ConfigHook(hooks.PecanHook):
    """Attach the configuration object to the request
    so controllers can get to it.
    """

    def before(self, state):
        state.request.cfg = cfg.CONF


class DBHook(hooks.PecanHook):

    def before(self, state):
        state.request.dbapi = dbapi.get_instance()
