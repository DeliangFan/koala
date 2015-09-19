#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from oslo.config import cfg

from sqlalchemy.orm.exc import NoResultFound

from koala.common import exception
from koala.common import utils
from koala.db import api
from koala.db.sqlalchemy import models
from koala.openstack.common.db.sqlalchemy import session as db_session
from koala.openstack.common import log
from koala.openstack.common import uuidutils

CONF = cfg.CONF
CONF.import_opt('connection',
                'koala.openstack.common.db.sqlalchemy.session',
                group='database')

LOG = log.getLogger(__name__)

get_engine = db_session.get_engine
get_session = db_session.get_session


def model_query(model, *args, **kwargs):
    """Query helper for simpler session usage.

    :param session: if present, the session to use
    """

    session = kwargs.get('session') or get_session()
    query = session.query(model, *args)
    return query


def get_backend():
    """The backend is this module itself."""
    return Connection()


def add_identity_filter(query, value):
    """Adds an identity filter to a query.

    Filters results by ID, if supplied value is a valid integer.
    Otherwise attempts to filter results by UUID.

    :param query: Initial query to add filter to.
    :param value: Value for filtering results by.
    :return: Modified query.
    """
    if utils.is_int_like(value):
        return query.filter_by(id=value)
    elif uuidutils.is_uuid_like(value):
        return query.filter_by(uuid=value)
    else:
        raise exception.InvalidIdentity(identity=value)


class Connection(api.Connection):
    def __init__(self):
        pass

    def price_get_by_id(self, id):
        """Get the price by id."""
        query = model_query(models.Price)
        query = add_identity_filter(query, id)

        return query.all()

    def price_get_all(self):
        """List the prices."""
        query = model_query(models.Price)

        return query.all()

    def price_create(self, value):
        """Create a new resource price."""
        price = models.Price()
        price.update(value)
        price.save()

        return price

    def price_update_by_id(self, id, value):
        """Update the price by id."""
        session = get_session()

        with session.begin():
            query = model_query(models.Price, session=session)
            query = add_identity_filter(query, id)
            count = query.update(value, synchronize_session='fetch')
            if count != 1:
                raise exception.PriceNotFound(ex)
            price = query.one()

        return price

    def price_delete_by_id(self, id):
        """Delete the price by id."""
        session = get_session()
        with session.begin():
            query = model_query(models.Price, session=session)
            query = add_identity_filter(query, id)
            count = query.delete()
            if count != 1:
                raise exception.PriceNotFound(ex)

    def resource_get_all(self):
        """List all the resources by query."""
        query = model_query(models.Resource)

        return query.all()

    def resource_get_by_id(self, resource_id):
        """Get the resource by id."""
        query = model_query(models.Resource)
        query = query.filter(models.Resource.resource_id==resource_id)

        return query.all()
