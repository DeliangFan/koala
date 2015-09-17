#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""The Example Service API."""

import logging
import sys

from oslo.config import cfg
from wsgiref import simple_server

from koala.api import app
from koala.common import service as koala_service
from koala.openstack.common import log

CONF = cfg.CONF


def main():
    # Pase config file and command line options, then start logging
    koala_service.prepare_service(sys.argv)

    # Build and start the WSGI app
    host = CONF.koala_api_bind_ip
    port = CONF.koala_api_port
    wsgi = simple_server.make_server(host,
                                     port,
                                     app.VersionSelectorApplication())

    LOG = log.getLogger(__name__)
    LOG.info("Serving on http://%s:%s" % (host, port))
    LOG.info("Configuration:")
    CONF.log_opt_values(LOG, logging.INFO)

    try:
        wsgi.serve_forever()
    except KeyboardInterrupt:
        pass
