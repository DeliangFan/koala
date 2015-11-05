# Copyright 2015 vanderliang@gmail.com
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


class TestInstanceEvent(base.FunctionalTest):

    def setUp(self):
        super(TestInstanceEvent, self).setUp()
        self.create_instance_price()

    def tearDown(self):
        super(TestInstanceEvent, self).tearDown()

    def create_instance_price(self):
        vcpu_price = utils.get_vcpu_price()
        ram_price = utils.get_ram_price()
        disk_price = utils.get_disk_price()
        self.post_json('/prices', vcpu_price).json
        self.post_json('/prices', ram_price).json
        self.post_json('/prices', disk_price).json

    def test_post_create_event_success(self):
        instance_event = utils.get_instance_event()
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        self.get_json(url, expect_errors=True)

        url = '/records/' + instance_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_exists_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_resize_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_type'] = 'resize'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_shut_off_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'shutoff')

        url = '/records/' + instance_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_power_on_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_type'] = 'power_on'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_create_and_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 720)

    def test_create_and_exist_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 720)

    def test_exists_and_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 720)

    def test_create_and_resize_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'create'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['content']['vcpu'] = 100
        instance_event['event_type'] = 'resize'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 720)

    def test_create_and_power_off_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'create'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'shutoff')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 720)

    def test_exists_and_power_off_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'shutoff')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 720)

    def test_power_off_and_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 240)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 240)

    def test_power_off_and_power_on_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'power_on'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 240)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 240)

    def test_create_exists_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'create'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 1440)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 720)
        self.assertEqual(int(records[1]['consumption']), 720)

    def test_create_resize_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'create'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['content']['vcpu'] = 1000
        instance_event['event_type'] = 'resize'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 241200)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 720)
        self.assertEqual(int(records[1]['consumption']), 240480)

    def test_exists_resize_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['content']['vcpu'] = 1000
        instance_event['event_type'] = 'resize'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 241200)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 720)
        self.assertEqual(int(records[1]['consumption']), 240480)

    def test_create_power_off_power_on_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'shutoff')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'power_on'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 960)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 720)
        self.assertEqual(int(records[1]['consumption']), 240)

    def test_create_power_off_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'shutoff')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 960)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 720)
        self.assertEqual(int(records[1]['consumption']), 240)

    def test_power_off_resize_vcpu_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['content']['vcpu'] = 10
        instance_event['event_type'] = 'resize'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 240)
        self.assertEqual(res['status'], 'shutoff')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 480)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 240)
        self.assertEqual(int(records[1]['consumption']), 240)

    def test_power_off_resize_disk_delete_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['content']['disk'] = 1000
        instance_event['event_type'] = 'resize'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 240)
        self.assertEqual(res['status'], 'shutoff')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 240240)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 240)
        self.assertEqual(int(records[1]['consumption']), 240000)

    def test_power_off_resize_disk_exists_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'power_off'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['content']['disk'] = 1000
        instance_event['event_type'] = 'resize'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 240)
        self.assertEqual(res['status'], 'shutoff')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 240240)
        self.assertEqual(res['status'], 'shutoff')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 240)
        self.assertEqual(int(records[1]['consumption']), 240000)

    def test_create_delete_create_event_success(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'create'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event, expect_errors=True)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 720)

    def test_create_exists_delete_with_missing_resize(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        instance_event['event_type'] = 'create'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-10-11T01:00:00.000000'
        # Missing resize event
        instance_event['content']['vcpu'] = 1000
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 720)

        instance_event['event_time'] = '2015-10-21T01:00:00.000000'
        instance_event['event_type'] = 'delete'
        self.post_json('/events', instance_event)

        url = '/resources/' + instance_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 241200)

        url = '/records/' + instance_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 720)
        self.assertEqual(int(records[1]['consumption']), 240480)

    def test_without_resource_id(self):
        instance_event = utils.get_instance_event()
        instance_event.pop('resource_id')
        self.post_json('/events', instance_event, expect_errors=True)

    def test_without_content(self):
        instance_event = utils.get_instance_event()
        instance_event.pop('content')
        self.post_json('/events', instance_event, expect_errors=True)

    def test_without_vcpu_in_content(self):
        instance_event = utils.get_instance_event()
        instance_event['content'].pop('vcpu')
        self.post_json('/events', instance_event, expect_errors=True)

    def test_with_wrong_vcpu_size_in_content(self):
        instance_event = utils.get_instance_event()
        instance_event['content']['vcpu'] = 'size'
        self.post_json('/events', instance_event, expect_errors=True)

        instance_event['content']['vcpu'] = -10
        self.post_json('/events', instance_event, expect_errors=True)

    def test_wrong_event_type(self):
        instance_event = utils.get_instance_event()
        instance_event['event_type'] = 'wrong_event_type'
        self.post_json('/events', instance_event, expect_errors=True)

    def test_with_wrong_event_time(self):
        instance_event = utils.get_instance_event()
        instance_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', instance_event)

        instance_event['event_time'] = '2015-09-11T01:00:00.000000'
        instance_event['event_type'] = 'exists'
        self.post_json('/events', instance_event, expect_errors=True)
