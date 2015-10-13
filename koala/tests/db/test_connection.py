#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from koala.db import api as dbapi
from koala.tests.db import base
from koala.tests.db import utils


class DbConnectionTestCase(base.DbTestCase):

    def setUp(self):
        super(DbConnectionTestCase, self).setUp()
        self.dbapi = dbapi.get_instance()

    def _create_test_price(self, **kwargs):
        price = utils.get_test_price(**kwargs)
        result = self.dbapi.price_create(price)
        return result

    def test_create_price(self):
        self._create_test_price()

    def test_get_price_by_id(self):
        price = self._create_test_price()
        res = self.dbapi.price_get_by_id(price['id'])
        self.assertEqual(price['id'], res['id'])

    def test_update_price(self):
        price = self._create_test_price()
        res = self.dbapi.price_update_by_id(price['id'], {'unit_price': 10})
        self.assertEqual(10, res['unit_price'])

    def test_destroy_price(self):
        price = self._create_test_price()

        self.dbapi.price_delete_by_id(price['id'])
        res = self.dbapi.price_get_by_id(price['id'])
        self.assertIsNone(res)
