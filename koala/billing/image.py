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

        self.unit_price = self.get_price()
        self.start_at = self.get_start_at()
        total_seconds = self.get_total_seconds(self.start_at, self.event_time)
        delta_time = total_seconds / 3600.0

        consumption = self.unit_price * delta_time * self.size

        return consumption
