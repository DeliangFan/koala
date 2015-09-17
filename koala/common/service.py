#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# filename   : service.py
# created at : 2013-07-01 12:23:11
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from oslo.config import cfg
from koala.openstack.common import log


def prepare_service(argv=[]):

    cfg.CONF(argv[1:], project='koala')
    log.setup('koala')
