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
    return Ex()


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


class Ex(api.Ex):

    def __init__(self):
        pass

    def get_ex(self, ex):
        query = model_query(models.Ex)
        query = add_identity_filter(query, ex)

        try:
            result = query.one()
        except NoResultFound:
            raise exception.ExNotFound(ex=ex)
        return result

    def get_exs(self):
        query = model_query(models.Ex)

        return query.all()

    def create_ex(self, values):
        if not values.get('uuid'):
            values['uuid'] = uuidutils.generate_uuid()
        ex = models.Ex()
        ex.update(values)
        ex.save()
        return ex

    def destroy_ex(self, ex):
        session = get_session()
        with session.begin():
            query = model_query(models.Ex, session=session)
            query = add_identity_filter(query, ex)
            count = query.delete()
            if count != 1:
                raise exception.ExNotFound(ex)

    def update_ex(self, ex, values):
        session = get_session()
        with session.begin():
            query = model_query(models.Ex, session=session)
            query = add_identity_filter(query, ex)
            count = query.update(values, synchronize_session='fetch')
            if count != 1:
                raise exception.ExNotFound(ex=ex)
            ref = query.one()
        return ref
