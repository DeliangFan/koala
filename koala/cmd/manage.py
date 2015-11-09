# -*- encoding: utf-8 -*-
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


"""
Run storage database migration.
"""
import sys

from koala.db import migration
from koala.openstack.common.gettextutils import _
from koala.openstack.common import log
from oslo.config import cfg


def add_command_parsers(subparsers):
    parser = subparsers.add_parser('db_version')

    parser = subparsers.add_parser('db_sync')
    parser.add_argument('version', nargs='?')
    parser.add_argument('current_version', nargs='?')

    parser = subparsers.add_parser('purge_deleted')
    parser.add_argument('age', nargs='?', default='90',
                        help=_('How long to preserve deleted data.'))
    parser.add_argument(
        '-g', '--granularity', default='days',
        choices=['days', 'hours', 'minutes', 'seconds'],
        help=_('Granularity to use for age argument, defaults to days.'))

command_opt = cfg.SubCommandOpt('command',
                                title='Commands',
                                help='Show available commands.',
                                handler=add_command_parsers)


def main():
    cfg.CONF.register_cli_opt(command_opt)
    try:
        cfg.CONF(sys.argv[1:], project='koala', prog='koala-manage')
        log.setup('koala')
    except RuntimeError as e:
        sys.exit("ERROR: %s" % e)

    version = None or sys.argv[2]
    try:
        migration.db_sync(version=version)
    except RuntimeError as e:
        sys.exit("ERROR: %s" % e)
