#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# filename   : api.py<2>
# created at : 2013-07-01 21:09:07


import abc

from koala.openstack.common.db import api as db_api

_BACKEND_MAPPING = {'sqlalchemy': 'koala.db.sqlalchemy.api'}
IMPL = db_api.DBAPI(backend_mapping=_BACKEND_MAPPING)


def get_instance():
    """Return a DB API instance."""
    return IMPL


class Connection(object):
    """Base db class."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        """Constructor"""

    @abc.abstractmethod
    def price_get_by_id(self, id):
        raise NotImplementedError('Prices not implemented.')
 
    @abc.abstractmethod
    def prices_get_all(self):
        raise NotImplementedError('Prices not implemented.')

    @abc.abstractmethod
    def price_create(self, value):
        raise NotImplementedError('Prices not implemented.')

    @abc.abstractmethod
    def price_update_by_id(self, id, value):
        raise NotImplementedError('Prices not implemented.')

    @abc.abstractmethod
    def price_delete_by_id(self, id):
        raise NotImplementedError('Prices not implemented.')

    @abc.abstractmethod
    def resources_get_all(self):
        raise NotImplementedError('Resources not implemented.')

    @abc.abstractmethod
    def resource_get_by_id(self, resource_id):
        raise NotImplementedError('Resources not implemented.')

    @abc.abstractmethod
    def resource_create(self, value):
        raise NotImplementedError('Resources not implemented.')

    @abc.abstractmethod
    def resource_update_by_id(self, resource_id, value):
        raise NotImplementedError('Resources not implemented.')

    @abc.abstractmethod
    def records_get_by_resource_id(self, resource_id):
        raise NotImplementedError('Records not implemented.')
