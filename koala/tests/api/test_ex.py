#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from koala.tests.api import base
from koala.tests.db import utils


class TestEx(base.FunctionalTest):

    def setUp(self):
        super(TestEx, self).setUp()

    def tearDown(self):
        super(TestEx, self).tearDown()

    def test_simple_create(self):
        json = self.post_json('/exs', utils.get_test_ex()).json
        expect = {
            "uuid": "1be26c0b-03f2-4d2e-ae87-c02d7f33c123",
            "title": "new ex",
            "content": "new content",
        }

        for key, value in expect.items():
            self.assertEqual(json[key], value)

        uri = '/exs/%s' % (json['uuid'])
        json = self.get_json(uri)

        for key, value in expect.items():
            self.assertEqual(json[key], value)

    def test_simple_update(self):
        json = self.post_json('/exs', utils.get_test_ex()).json
        uri = '/exs/%s' % (json['uuid'])
        self.put_json(uri, utils.get_test_ex(title="update"))
        json = self.get_json(uri)
        self.assertEqual(json['title'], "update")

    def test_simple_delete(self):
        json = self.post_json('/exs', utils.get_test_ex()).json
        uri = '/exs/%s' % (json['uuid'])
        self.delete(uri)
        response = self.get_json(uri, expect_errors=True)
        self.assertEqual(response.status_int, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertTrue(response.json['error_message'])
