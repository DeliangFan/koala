# Copyright 2015 vanderliang@gmail.com.
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

import copy
import json
import requests
import unittest


OK_STATUS = (200, 201, 202, 204)


class TestPrice(unittest.TestCase):

    def setUp(self):
        self.url = "http://127.0.0.1:9999/v1/prices"
        self.headers = {'content-type': 'application/json'}
        self.body = {
            'resource_type': 'instance',
            'region': 'regionOne',
            'unit_price': 0.888}

    def test_create_get_and_delete_price(self):
        # Create price
        body = copy.deepcopy(self.body)
        res = requests.post(self.url, data=json.dumps(body),
                            headers=self.headers)
        self.assertIn(res.status_code, OK_STATUS)

        # Get the price by id
        res_body = json.loads(res.text)
        price_id = res_body['id']
        url = self.url + '/' + str(price_id)

        res = requests.get(url)
        res_body = json.loads(res.text)
        self.assertIn(res.status_code, OK_STATUS)
        self.assertEqual(res_body['resource_type'], 'instance')

        # Delete price
        res = requests.delete(url)
        self.assertIn(res.status_code, OK_STATUS)

    def test_create_with_invalid_body(self):
        body = copy.deepcopy(self.body)
        body.pop('resource_type')
        res = requests.post(self.url, data=json.dumps(body),
                            headers=self.headers)
        self.assertEqual(res.status_code, 400)

        body = copy.deepcopy(self.body)
        body.pop('region')
        res = requests.post(self.url, data=json.dumps(body),
                            headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_update_price(self):
        # Create price
        body = self.body
        res = requests.post(self.url, data=json.dumps(body),
                            headers=self.headers)
        self.assertIn(res.status_code, OK_STATUS)

        # Test update the price by price id
        res_body = json.loads(res.text)
        body = {'unit_price': 8888, 'id': res_body['id']}
        res = requests.put(self.url, data=json.dumps(body),
                           headers=self.headers)
        self.assertIn(res.status_code, OK_STATUS)
        res_body = json.loads(res.text)
        self.assertEqual(res_body['unit_price'], 8888)

        # Delete price
        url = self.url + '/' + str(res_body['id'])
        res = requests.delete(url)
        self.assertIn(res.status_code, OK_STATUS)


if __name__ == '__main__':
    unittest.main()
