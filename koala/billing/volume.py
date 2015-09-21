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

VOLUME_EVENT_TYPES = ('create', 'delete', 'resize', 'exists')


class Volume(base.Resource):
    """Volume billing resource."""

    def __init__(self, value):
        super(Volume, self).__init__(value)

        self.size = self.content.get('size', None)
        self.check_event_type()
        self.check_content()

    def check_event_type(self):
        if self.event_type not in VOLUME_EVENT_TYPES:
            msg = _("Volume event type must be in %s") % str(VOLUME_EVENT_TYPES)
            raise exception.EventTypeInvalid(msg)

    def check_content(self):
        self.size = self.content.get('size', None)

        if self.size is None:
            msg = _("Volume size not specified in the content.")
            raise exception.VolumeContentInvalid(msg)

        if self.size < 1:
            msg = _("Volume size must be positive integer.")
            raise exception.VolumeSizeInvalid(msg)

    def billing_resource(self):
        """Billing resource

           This is the mainly function for billing a resource. When the new event
           comes, we check whether the resource is a new or not. If it's a new
           resource, we need to generate a resource corresponding, otherwise, we
           just to calculate the consumption and update the billing records.
        """
        if self.get_resource():
            self.calculate_consumption()
        else:
            # NOTE(fandeliang) we still need to check the event type. if the event
            # type is not create, it means that some messages ahead have lost.
            self.create_resource()

    def calculate_consumption(self):
        pass
