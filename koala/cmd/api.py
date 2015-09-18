#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""The Koala Service API."""

import logging
import sys

from oslo.config import cfg
from wsgiref import simple_server

from koala.api import app
from koala.common import service as koala_service
from koala.openstack.common import log

service_opts = [
    cfg.StrOpt('host',
                default='0.0.0.0',
                help='Koala api bind ip.'),
    cfg.IntOpt('port',
                default=9999,
                help='Koala api bind port.'),
]

CONF = cfg.CONF
CONF.register_opts(service_opts)


def main():
    # Pase config file and command line options, then start logging
    koala_service.prepare_service(sys.argv)

    # Build and start the WSGI app
    host = CONF.host
    port = CONF.port
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
