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

EVENT_TYPES = ('upload', 'delete', 'exists')


class Image(base.Resource):
    """Image billing resource.

       We have two kinds of image, one is called public image and the other
       is private image. Public image is visiable to every tenant and can
       be created by administrator which should not be billed. While private
       image is created by user and owned by user which should be billed.

       NOTE: Koala treat al the image event as private image.
    """
    def __init__(self, value):
        self.EVENT_TYPES = EVENT_TYPES

        super(Image, self).__init__(value)

        self.size = self.content.get('size', None)
        self.check_content()

    def check_content(self):
        if self.size is None:
            msg = _("Image size not specified in the content.")
            raise exception.ImageContentInvalid(msg)

        if self.size < 1:
            msg = _("Image size must be positive integer.")
            raise exception.ImageSizeInvalid(msg)

    def calculate_consumption(self):
        """Calculate the consumption by deta time and price."""
        resource = self.get_resource()
        unit_price = self.get_price()
        start_at = self.get_start_at()
        deta_time = (self.event_time - start_at).total_seconds() / 3600.0

        record = {}
        updated_resource = {}
        record_description = self.resource_type + ' ' + self.event_type

        if self.event_type == 'upload':
            msg = _("Duplicate event.")
            raise exception.EventDuplicate(msg)
        elif self.event_type == 'exists':
            record_description = "Audit billing"
        elif self.event_type == 'delete':
            updated_resource['deleted'] = 1
            updated_resource['deleted_at'] = self.event_time
            updated_resource['status'] = 'delete'
            updated_resource['description'] = "Resource has ben deleted."

        consumption = unit_price * deta_time * self.size

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
