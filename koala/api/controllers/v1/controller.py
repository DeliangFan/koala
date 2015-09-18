#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import datetime

import pecan
from pecan import rest

from koala.api.controllers.v1 import base
from koala.common import exception
from koala.common.wsmeext import pecan as wsme_pecan
from koala.db import api as db_api
from koala.openstack.common.gettextutils import _
from wsme import types as wtypes

REQUEIRED_PRICE_PROPERTIES = ('name', 'region', 'resource_type', 'unit_price')


class Price(base.APIBase):
    "The id of the resource price."
    id = int
    unit_price = float
    name = wtypes.text
    region = wtypes.text
    description = wtypes.text
    resource_type = wtypes.text
    created_at = datetime.datetime
    updated_at = datetime.datetime

    @classmethod
    def sample(cls):
        return cls(
            id=1,
            name='sata_disk',
            region='bj',
            unit_price=0.8,
            resource_type='volume',
            created_at="2015-09-18T08:46:54.349148",
            updated_at="2015-09-19T08:46:54.349148",
            description='Price of sata volume.'
        )


class PricesController(rest.RestController):

    @wsme_pecan.wsexpose(Price, int)
    def get_one(self, id):
        """Get the resource price by id."""
        prices = pecan.request.dbapi.price_get_by_id(id)
        if not prices:
            msg = _("Price %s not found.") % str(id)
            raise exception.PriceNotFound(msg)

        return prices[0]

    @wsme_pecan.wsexpose([Price])
    def get_all(self):
        """Return all the price of resources."""
        prices = pecan.request.dbapi.price_get_all()

        return prices

    @wsme_pecan.wsexpose(Price, body=Price, status_code=201)
    def post(self, data):
        """Create a new resource price."""
        value = data.as_dict()

        for key in REQUEIRED_PRICE_PROPERTIES:
            if key not in value:
                msg = _("Property %s is required by the price.") % key
                raise exception.Invalid(msg)

        id = value.get('id', None)
        if id:
            existed_price = pecan.request.dbapi.price_get_by_id(id)
            if existed_price:
                msg = _("Price %s already exists.") % str(id)
                raise exception.PriceIdConflict(msg)

        """Create the price of the resource."""
        price = pecan.request.dbapi.price_create(value)

        return price

    @wsme_pecan.wsexpose(Price, body=Price)
    def put(self, data):
        """Modify the resource price."""
        value = data.as_dict()

        id = value.get('id', None)
        if not id:
            msg = _("Property id is required by the price.")
            raise exception.Invalid(msg)
        else:
            existed_price = pecan.request.dbapi.price_get_by_id(id)
            if not existed_price:
                msg = _("Price %s not found.") % str(id)
                raise exception.PriceNotFound(msg)

        price = pecan.request.dbapi.price_update_by_id(id, value)

        return price

    @wsme_pecan.wsexpose(None, int, status_code=204)
    def delete(self, id):
        """Delete the resource price by id."""
        prices = pecan.request.dbapi.price_get_by_id(id)
        if not prices:
            msg = _("Price %s not found.") % str(id)
            raise exception.PriceNotFound(msg)

        pecan.request.dbapi.price_delete_by_id(id)


class Controller(object):
    """Version 1 API controller root."""

    prices = PricesController()
