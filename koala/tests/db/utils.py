# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 UnitedStack Inc.
# All Rights Reserved
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


def get_test_price(**kw):
    price = {
        'resource_type': kw.get('resource_type', 'volume'),
        'unit_price': kw.get('unit_price', 1),
        'region': kw.get('region', 'regionOne')
    }
    return price


def get_volume_price(**kw):
    price = get_test_price(**kw)
    return price


def get_volume_snapshot_price(**kw):
    price = get_test_price(**kw)
    price['resource_type'] = 'volume_snapshot'

    return price


def get_image_price(**kw):
    price = get_test_price(**kw)
    price['resource_type'] = 'image'

    return price


def get_instance_snapshot_price(**kw):
    price = get_test_price(**kw)
    price['resource_type'] = 'instance_snapshot'

    return price


def get_router_price(**kw):
    price = get_test_price(**kw)
    price['resource_type'] = 'router'

    return price


def get_volume_event(**kw):
    volume_event = {
        'resource_id': kw.get('resource_id',
                              'ea75b3e1-e3b6-4777-bc4e-ef6ea414ace2'),
        'resource_name': kw.get('resource_name', 'volume01'),
        'resource_type': kw.get('resource_type', 'volume'),
        'event_type': kw.get('event_type', 'create'),
        'event_time': kw.get('event_time', '2015-10-01T01:00:00.000000'),
        'tenant_id': kw.get('tenant_id', '7f13f2b17917463b9ee21aa92c4b36d6'),
        'region': kw.get('region', 'regionOne'),
        'content': kw.get('content', {'size': 10})
    }

    return volume_event


def get_volume_snapshot_event(**kw):
    volume_snapshot_event = get_volume_event(**kw)
    volume_snapshot_event['resource_name'] = 'volume_snapshot01'
    volume_snapshot_event['resource_type'] = 'volume_snapshot'

    return volume_snapshot_event


def get_image_event(**kw):
    image_event = get_volume_event(**kw)
    image_event['event_type'] = 'upload'
    image_event['resource_name'] = 'image01'
    image_event['resource_type'] = 'image'

    return image_event


def get_instance_snapshot_event(**kw):
    instance_snapshot_event = get_volume_event(**kw)
    instance_snapshot_event['event_type'] = 'upload'
    instance_snapshot_event['resource_name'] = 'instance_snapshot01'
    instance_snapshot_event['resource_type'] = 'instance_snapshot'

    return instance_snapshot_event


def get_router_event(**kw):
    router_event = get_volume_event(**kw)
    router_event['resource_name'] = 'router01'
    router_event['resource_type'] = 'router'
    router_event['content'] = {}

    return router_event
