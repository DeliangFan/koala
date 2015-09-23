#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from koala.common import exception
from koala.db import api as dbapi
from koala.openstack.common import uuidutils
from koala.tests.db import base
from koala.tests.db import utils


class DbExTestCase(base.DbTestCase):

    def setUp(self):
        super(DbExTestCase, self).setUp()
        self.dbapi = dbapi.get_instance()

    def _create_test_ex(self, **kwargs):
        c = utils.get_test_ex(**kwargs)
        self.dbapi.create_ex(c)
        return c

    def test_create_ex(self):
        self._create_test_ex()

    def test_get_ex_by_id(self):
        c = self._create_test_ex()
        res = self.dbapi.get_ex(c['id'])
        self.assertEqual(c['uuid'], res['uuid'])

    def test_get_ex_by_uuid(self):
        c = self._create_test_ex()
        res = self.dbapi.get_ex(c['uuid'])
        self.assertEqual(c['id'], res['id'])

    def test_update_ex(self):
        c = self._create_test_ex()
        res = self.dbapi.get_ex(c['id'])

        old_title = c['title']
        new_title = 'ex'
        self.assertNotEqual(old_title, new_title)

        res = self.dbapi.update_ex(c['id'], {'title': new_title})
        self.assertEqual(new_title, res['title'])

    def test_destroy_ex(self):
        c = self._create_test_ex()

        self.dbapi.destroy_ex(c['id'])
        self.assertRaises(exception.ExNotFound,
                          self.dbapi.get_ex, c['id'])

    def test_get_exs(self):
        uuids = []
        for i in xrange(1, 6):
            c = utils.get_test_ex(id=i, uuid=uuidutils.generate_uuid())
            self.dbapi.create_ex(c)
            uuids.append(unicode(c['uuid']))
        res = self.dbapi.get_exs()
        reid = []
        for re in res:
            reid.append(re['uuid'])
        uuids.sort()
        reid.sort()
        self.assertEqual(uuids, reid)
        return uuids
