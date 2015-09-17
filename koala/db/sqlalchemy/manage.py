#!/usr/bin/env python

from oslo.config import cfg

from migrate.versioning.shell import main

CONF = cfg.CONF
CONF.import_opt('connection',
                'koala.openstack.common.db.sqlalchemy.session',
                group='database')

if __name__ == '__main__':
    main(url=CONF.database.connection,
            debug='False', repository='migrate_repo')
