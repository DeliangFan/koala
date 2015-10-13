# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from koala.tests.api import base
from koala.tests.db import utils

PRICE_DATA = {
    "resource_type": "volume",
    "region": "regionOne",
    "unit_price": 1}


class TestPrice(base.FunctionalTest):

    def setUp(self):
        super(TestPrice, self).setUp()

    def tearDown(self):
        super(TestPrice, self).tearDown()

    def test_price_create(self):
        json = self.post_json('/prices', PRICE_DATA).json
        expect = {
            "resource_type": "volume",
            "region": "regionOne",
            "unit_price": 1
        }

        for key, value in expect.items():
            self.assertEqual(json[key], value)

        uri = '/prices/' + str(json['id'])
        json = self.get_json(uri)

        for key, value in expect.items():
            self.assertEqual(json[key], value)

    def test_price_update(self):
        json = self.post_json('/prices', PRICE_DATA).json
        uri = '/prices/%s' % (json['id'])
        self.put_json('/prices', {'id': json['id'], 'unit_price': 2})
        json = self.get_json(uri)
        self.assertEqual(json['unit_price'], 2)

    def test_simple_delete(self):
        json = self.post_json('/prices', PRICE_DATA).json
        uri = '/prices/%s' % (json['id'])
        self.delete(uri)
        response = self.get_json(uri, expect_errors=True)
        self.assertEqual(response.status_int, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertTrue(response.json['error_message'])
