#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from koala.common import exception
from koala.common import utils
from koala.db import api
from koala.db.sqlalchemy import models
from koala.openstack.common.db.sqlalchemy import session as db_session
from koala.openstack.common.gettextutils import _
from koala.openstack.common import log
from koala.openstack.common import uuidutils

from oslo.config import cfg

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

    def price_get_by_resource(self, resource_type, region):
        """Get the price by resource type and region."""
        query = model_query(models.Price)
        query = query.filter(models.Price.resource_type == resource_type)
        query = query.filter(models.Price.region == region)

        prices = query.all()
        if prices:
            price = prices[0]
        else:
            price = None

        return price

    def prices_get_all(self):
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
                msg = _("Price %s not found.") % str(id)
                raise exception.PriceNotFound(msg)
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
                msg = ("Price %s not found.") % str(id)
                raise exception.PriceNotFound(msg)

    def resources_get_all(self):
        """List all the resources by query."""
        query = model_query(models.Resource)

        return query.all()

    def resource_get_by_id(self, resource_id):
        """Get the resource by id."""
        query = model_query(models.Resource)
        query = query.filter(models.Resource.resource_id == resource_id)

        return query.all()

    def resource_create(self, value):
        """Create a new resource."""
        resource = models.Resource()
        resource.update(value)
        resource.save()

        return resource

    def resource_update_by_id(self, resource_id, value):
        """Update the resource by id."""
        session = get_session()

        with session.begin():
            query = model_query(models.Resource, session=session)
            query = query.filter(models.Resource.resource_id == resource_id)
            count = query.update(value, synchronize_session='fetch')

            if count != 1:
                msg = _("Resource %s not found.") % resource_id
                raise exception.ResourceNotFound(msg)

            resource = query.one()
        return resource

    def records_get_by_resource_id(self, resource_id):
        """List the records by resource id."""
        query = model_query(models.Record)
        query = query.filter(models.Record.resource_id == resource_id)

        return query.all()

    def record_get_by_last(self, resource_id):
        """Get the last record by resource id."""
        query = model_query(models.Record)
        query = query.filter(models.Record.resource_id == resource_id)

        # Get the lastest record by record end_at timestamp.
        resource = query.order_by(models.Record.end_at.desc(),
                                  models.Record.id.desc()).limit(1).all()

        if not resource:
            return None

        return resource[0]

    def record_create(self, value):
        """Create a new record."""
        record = models.Record()
        record.update(value)
        record.save()

        return record
