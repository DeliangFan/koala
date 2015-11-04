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


class TestImageEvent(base.FunctionalTest):

    def setUp(self):
        super(TestImageEvent, self).setUp()
        self.create_image_price()

    def tearDown(self):
        super(TestImageEvent, self).tearDown()

    def create_image_price(self):
        self.post_json('/prices', utils.get_image_price()).json

    def test_post_upload_event_success(self):
        image_event = utils.get_image_event()
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 0)

        url = '/records/' + image_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_exists_event_success(self):
        image_event = utils.get_image_event()
        image_event['event_type'] = 'exists'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 0)

        url = '/records/' + image_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_post_delete_event_success(self):
        image_event = utils.get_image_event()
        image_event['event_type'] = 'delete'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        self.get_json(url, expect_errors=True)

        url = '/records/' + image_event['resource_id']
        self.get_json(url, expect_errors=True)

    def test_upload_delete_event_success(self):
        image_event = utils.get_image_event()
        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', image_event)

        image_event['event_type'] = 'delete'
        image_event['event_time'] = '2015-10-11T01:00:00.000000'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 2400)

        url = '/records/' + image_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_exists_delete_event_success(self):
        image_event = utils.get_image_event()
        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        image_event['event_type'] = 'exists'
        self.post_json('/events', image_event)

        image_event['event_type'] = 'delete'
        image_event['event_time'] = '2015-10-11T01:00:00.000000'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 2400)

        url = '/records/' + image_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_upload_exists_event_success(self):
        image_event = utils.get_image_event()
        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', image_event)

        image_event['event_type'] = 'exists'
        image_event['event_time'] = '2015-10-11T01:00:00.000000'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 2400)

        url = '/records/' + image_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_exits_exists_event_success(self):
        image_event = utils.get_image_event()
        image_event['event_type'] = 'exists'
        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', image_event)

        image_event['event_type'] = 'exists'
        image_event['event_time'] = '2015-10-11T01:00:00.000000'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 2400)

        url = '/records/' + image_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_upload_exists_delete_event_success(self):
        image_event = utils.get_image_event()
        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', image_event)

        image_event['event_type'] = 'exists'
        image_event['event_time'] = '2015-10-11T01:00:00.000000'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 2400)

        image_event['event_type'] = 'delete'
        image_event['event_time'] = '2015-10-21T01:00:00.000000'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 4800)

        url = '/records/' + image_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 2400)
        self.assertEqual(int(records[1]['consumption']), 2400)

    def test_exists_exists_delete_event_success(self):
        image_event = utils.get_image_event()
        image_event['event_type'] = 'exists'
        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', image_event)

        image_event['event_type'] = 'exists'
        image_event['event_time'] = '2015-10-11T01:00:00.000000'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'active')
        self.assertEqual(int(res['consumption']), 2400)

        image_event['event_type'] = 'delete'
        image_event['event_time'] = '2015-10-21T01:00:00.000000'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 4800)

        url = '/records/' + image_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 2)
        self.assertEqual(int(records[0]['consumption']), 2400)
        self.assertEqual(int(records[1]['consumption']), 2400)

    def test_upload_delete_exists_event_success(self):
        image_event = utils.get_image_event()
        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', image_event)

        image_event['event_type'] = 'delete'
        image_event['event_time'] = '2015-10-11T01:00:00.000000'
        self.post_json('/events', image_event)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 2400)

        image_event['event_type'] = 'exists'
        image_event['event_time'] = '2015-10-21T01:00:00.000000'
        self.post_json('/events', image_event, expect_errors=True)

        url = '/resources/' + image_event['resource_id']
        res = self.get_json(url)
        self.assertEqual(res['status'], 'delete')
        self.assertEqual(int(res['consumption']), 2400)

        url = '/records/' + image_event['resource_id']
        records = self.get_json(url)
        self.assertEqual(len(records), 1)
        self.assertEqual(int(records[0]['consumption']), 2400)

    def test_without_resource_id(self):
        image_event = utils.get_image_event()
        image_event.pop('resource_id')
        self.post_json('/events', image_event, expect_errors=True)

    def test_without_tenant_id(self):
        image_event = utils.get_image_event()
        image_event.pop('tenant_id')
        self.post_json('/events', image_event, expect_errors=True)

    def test_without_content(self):
        image_event = utils.get_image_event()
        image_event.pop('content')
        self.post_json('/events', image_event, expect_errors=True)

    def test_without_wrong_content(self):
        image_event = utils.get_image_event()
        image_event.pop('content')
        self.post_json('/events', image_event, expect_errors=True)

    def test_without_wrong_size_in_content(self):
        image_event = utils.get_image_event()
        image_event['content']['size'] = 'wrong_size'
        self.post_json('/events', image_event, expect_errors=True)

    def test_without_wrong_type(self):
        image_event = utils.get_image_event()
        image_event['event_type'] = 'create'
        self.post_json('/events', image_event, expect_errors=True)

    def test_with_wrong_event_time(self):
        image_event = utils.get_image_event()
        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', image_event)

        image_event['event_type'] = 'exists'
        image_event['event_time'] = '2015-09-01T01:00:00.000000'
        self.post_json('/events', image_event, expect_errors=True)

    def test_upload_upload_event_fail(self):
        image_event = utils.get_image_event()
        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', image_event)

        image_event['event_time'] = '2015-10-01T01:00:00.000000'
        self.post_json('/events', image_event, expect_errors=True)
