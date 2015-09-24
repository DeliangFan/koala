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
from koala.openstack.common import jsonutils

EVENT_TYPES = ('create', 'delete', 'resize', 'exists', 'power_off',
               'power_on')
# INSTANCE_STATUS = ('active', 'shutoff', 'delete')


class Instance(base.Resource):
    """Instance billing system."""
    # NOTE(fandeliang) we need to consider more kinds of instance status.

    def __init__(self, value):
        self.EVENT_TYPES = EVENT_TYPES

        super(Instance, self).__init__(value)

        self.vcpu = self.content.get('vcpu', None)
        self.ram = self.content.get('ram', None)
        self.disk = self.content.get('disk', None)

        self.check_content()

    def check_content(self):

        for key in ('vcpu', 'ram', 'disk'):
            value = self.content.get(key, None)

            if value is None:
                msg = _("%s not specified in the content.") % key.title()
                raise exception.InstanceContentInvalid(msg)

            if value < 1:
                msg = _(" must be positive integer.") % key.title()
                raise exception.InstanceContentInvalid(msg)

    def get_instance_price(self):
        """Get the vcpu, ram and disk price of instance."""

        instance_price = {}

        instance_price['vcpu'] = self.get_price(resource_type='vcpu')
        instance_price['ram'] = self.get_price(resource_type='ram')
        instance_price['disk'] = self.get_price(resource_type='disk')

        return instance_price

    def get_instance_previous_status(self):
        """Get the previous status."""

        previous_status = self.exist_resource.status
        if not previous_status:
            previous_status = 'active'

        return previous_status

    def calculate_consumption(self):
        """Calculate the consumption by delta time and price."""
        # Note(fandeliang) for instance, we should care the status.

        self.instance_price = self.get_instance_price()
        self.start_at = self.get_start_at()
        total_seconds = self.get_total_seconds(self.start_at, self.event_time)
        delta_time = total_seconds / 3600.0

        if self.event_type == 'resize':
            pre_content = jsonutils.loads(self.exist_resource.content)
            vcpu = pre_content.get('vcpu', 0)
            ram = pre_content.get('ram', 0)
            disk = pre_content.get('disk', 0)
        else:
            vcpu = self.vcpu
            ram = self.ram
            disk = self.disk

        previous_status = self.get_instance_previous_status()

        # If the instance is shut off, we only billing the disk costs.
        if previous_status == 'shutoff':
            self.unit_price = self.instance_price['disk'] * disk
        else:
            self.unit_price = self.instance_price['vcpu'] * vcpu
            self.unit_price += self.instance_price['ram'] * ram
            self.unit_price += self.instance_price['disk'] * disk

        consumption = self.unit_price * delta_time

        return consumption
