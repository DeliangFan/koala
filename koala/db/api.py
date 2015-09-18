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
        raise NotImplementedError('Prices not implemented')
 
    @abc.abstractmethod
    def price_get_all(self):
        raise NotImplementedError('Prices not implemented')

    @abc.abstractmethod
    def price_create(self, data):
        raise NotImplementedError('Prices not implemented')

    @abc.abstractmethod
    def price_update_by_id(self, id, value):
        raise NotImplementedError('Prices not implemented')

    @abc.abstractmethod
    def price_delete_by_id(self, id):
        raise NotImplementedError('Prices not implemented')


class Ex(object):
    """Base db class."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        """Constructor"""

    @abc.abstractmethod
    def get_ex(self, ex):
        """get ex by uuid of and uuid of its ex.

        :param ex: uuid of the ex
        :return: a list of exs
        """

    @abc.abstractmethod
    def get_exs(self):
        """get list of exs by uuid

        :return: a dict of values of the ex
        """

    @abc.abstractmethod
    def create_ex(self, values):
        """create a ex

        :param values: a dict of ex data
        :return: a dict of newly created ex data
        """

    @abc.abstractmethod
    def destroy_ex(self, ex):
        """delete a ex

        :param ex: uuid of the ex
        """

    @abc.abstractmethod
    def update_ex(self, ex, values):
        """update a ex

        :param ex: uuid of the ex
        :param values: a dict of update values
        :return: a dict of newly updated ex
        """
