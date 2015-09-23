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

from koala.billing import base
from koala.common import exception
from koala.openstack.common.gettextutils import _

EVENT_TYPES = ('create', 'delete', 'exists')


class Router(base.Resource):
    """Router billing resource."""

    def __init__(self, value):
        self.EVENT_TYPES = EVENT_TYPES

        super(Router, self).__init__(value)
        self.check_content()

    def check_content(self):

        # For router, we only care the usage time and unit_price, so the
        # content should be a empty dict.
        if self.content:
            msg = _("Router content should be empty.")
            raise exception.RouterContentInvalid(msg)

    def calculate_consumption(self):
        """Calculate the consumption by deta time and price."""
        resource = self.get_resource()
        unit_price = self.get_price()
        start_at = self.get_start_at()
        deta_time = self.get_total_seconds(start_at, self.event_time) / 3600.0
        record = {}
        updated_resource = {}
        record_description = self.resource_type + ' ' + self.event_type

        if self.event_type == 'create':
            msg = _("Duplicate event.")
            raise exception.EventDuplicate(msg)
        elif self.event_type == 'exists':
            record_description = "Audit billing"
        elif self.event_type == 'delete':
            updated_resource['deleted'] = 1
            updated_resource['deleted_at'] = self.event_time
            updated_resource['status'] = 'delete'
            updated_resource['description'] = "Router has ben deleted."

        consumption = unit_price * deta_time

        # Format record information and store it to database.
        record['resource_id'] = self.resource_id
        record['start_at'] = start_at
        record['end_at'] = self.event_time
        record['unit_price'] = unit_price
        record['consumption'] = consumption
        record['description'] = record_description
        self.create_record(record)

        # Format resource information and update it to database.
        updated_resource['consumption'] = resource.consumption + consumption
        self.update_resource(updated_resource)
