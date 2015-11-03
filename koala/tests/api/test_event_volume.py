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


class TestVolumeEvent(base.FunctionalTest):

    def setUp(self):
        super(TestVolumeEvent, self).setUp()

    def tearDown(self):
        super(TestVolumeEvent, self).tearDown()

    def create_volume_price(self):
        body = self.post_json('/prices', utils.get_volume_price()).json
        return body['id']

    def test_post_create_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + volume_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_delete_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_type'] = 'delete'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        self.get_json(url, expect_errors=True)

        url = '/records/' + volume_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_exists_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_type'] = 'exists'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + volume_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_resize_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_type'] = 'resize'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + volume_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_create_and_delete_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-10-11T01:00:00.000000'
        volume_event['event_type'] = 'delete'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_create_and_exist_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-10-11T01:00:00.000000'
        volume_event['event_type'] = 'exists'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_exists_and_delete_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        volume_event['event_type'] = 'exists'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-10-11T01:00:00.000000'
        volume_event['event_type'] = 'delete'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_create_and_resize_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        volume_event['event_type'] = 'create'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-10-11T01:00:00.000000'
        volume_event['content']['size'] = 200
        volume_event['event_type'] = 'resize'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_create_exists_delete_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        volume_event['event_type'] = 'create'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-10-11T01:00:00.000000'
        volume_event['event_type'] = 'exists'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        volume_event['event_time'] = '2015-10-21T01:00:00.000000'
        volume_event['event_type'] = 'delete'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 4800)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 2400)
        self.assertEqual(int(records[1]['consumption']), 2400)

    def test_create_resize_delete_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        volume_event['event_type'] = 'create'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-10-11T01:00:00.000000'
        volume_event['content']['size'] = 1000
        volume_event['event_type'] = 'resize'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        volume_event['event_time'] = '2015-10-21T01:00:00.000000'
        volume_event['event_type'] = 'delete'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 242400)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 2400)
        self.assertEqual(int(records[1]['consumption']), 240000)

    def test_exists_resize_delete_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        volume_event['event_type'] = 'exists'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-10-11T01:00:00.000000'
        volume_event['content']['size'] = 1000
        volume_event['event_type'] = 'resize'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)
        self.assertEqual(res['status'], 'active')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        volume_event['event_time'] = '2015-10-21T01:00:00.000000'
        volume_event['event_type'] = 'delete'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 242400)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 2400)
        self.assertEqual(int(records[1]['consumption']), 240000)

    def test_create_delete_create_event_success(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        volume_event['event_type'] = 'create'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-10-11T01:00:00.000000'
        volume_event['event_type'] = 'delete'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)

        volume_event['event_time'] = '2015-10-21T01:00:00.000000'
        volume_event['event_type'] = 'exists'
        self.post_json('/events', volume_event, expect_errors=True)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)
        self.assertEqual(res['status'], 'delete')

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_create_exists_delete_with_missing_resize(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        volume_event['event_type'] = 'create'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-10-11T01:00:00.000000'
        # Missing resize event
        volume_event['content']['size'] = 1000
        volume_event['event_type'] = 'exists'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 2400)

        volume_event['event_time'] = '2015-10-21T01:00:00.000000'
        volume_event['event_type'] = 'delete'
        self.post_json('/events', volume_event)

        url = '/resources/' + volume_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(int(res['consumption']), 242400)

        url = '/records/' + volume_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 2400)
        self.assertEqual(int(records[1]['consumption']), 240000)

    def test_without_resource_id(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event.pop('resource_id')
        self.post_json('/events', volume_event, expect_errors=True)

    def test_without_content(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event.pop('content')
        self.post_json('/events', volume_event, expect_errors=True)

    def test_without_size_in_content(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['content'].pop('size')
        self.post_json('/events', volume_event, expect_errors=True)

    def test_with_wrong_size_in_content(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['content']['size'] = 'size'
        self.post_json('/events', volume_event, expect_errors=True)

        volume_event['content']['size'] = -10
        self.post_json('/events', volume_event, expect_errors=True)

    def test_wrong_event_type(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_type'] = 'wrong_event_type'
        self.post_json('/events', volume_event, expect_errors=True)

    def test_with_wrong_event_time(self):
        self.create_volume_price()

        volume_event = utils.get_volume_event()
        volume_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', volume_event)

        volume_event['event_time'] = '2015-09-11T01:00:00.000000'
        volume_event['event_type'] = 'exists'
        self.post_json('/events', volume_event, expect_errors=True)
