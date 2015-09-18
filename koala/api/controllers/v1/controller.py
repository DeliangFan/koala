#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import pecan
from pecan import rest

from koala.api.controllers.v1 import base
from koala.common.wsmeext import pecan as wsme_pecan
from koala.db import api as db_api
from wsme import types as wtypes


class Price(base.APIBase):
    "The id of the resource price."
    id = int
    name = wtypes.text
    resource_type = wtypes.text
    unit_price = float
    region = wtypes.text
    description = wtypes.text

    @classmethod
    def sample(cls):
        return cls(
            id=1,
            name='sata_disk',
            resource_type='volume',
            unit_price=0.8,
            region='bj',
            description='Price of sata volume!'
        )


class PricesController(rest.RestController):

    @wsme_pecan.wsexpose(Price, int)
    def get_one(self, id):
        """Get the resource price by id."""
        prices = list(pecan.request.dbapi.price_get_by_id(id))
        if len(prices) < 1:
            raise NotFound
        return prices[0]

    @wsme_pecan.wsexpose([Price])
    def get_all(self):
        """Return all the price of resources."""
        # TBD(fandeliang) Get all the price from db.
        return [Price.sample()]

    @wsme_pecan.wsexpose(Price, body=Price, status_code=201)
    def post(self, data):
        """Create a new resource price."""
        # TBD(fandeliang) Create a new resource price in db.
        return Price.sample()

    @wsme_pecan.wsexpose(Price, int, body=Price)
    def put(self, id, data):
        """Modify the resource price."""
        # TBD(fandeliang) Modify the resource price
        return Price.sample()

    @wsme_pecan.wsexpose(None, int, status_code=204)
    def delete(self, id):
        """Delete the resource price by id."""
        # TBD(fandeliang) Delete the resource price from db.
        pass


class Controller(object):
    """Version 1 API controller root."""

    prices = PricesController()
