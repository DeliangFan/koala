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

from koala.billing import image
from koala.common import exception
from koala.openstack.common.gettextutils import _

EVENT_TYPES = ('upload', 'delete', 'exists')


class InstanceSnapshot(image.Image):
    """Instance snapshot billing resource.

       Instance snapshot is the copy of instance disk and stored as an image
       in glance.
    """
    def __init__(self, value):
        super(InstanceSnapshot, self).__init__(value)

    def check_content(self):
        if self.size is None:
            msg = _("Instance snapshot size not specified in the content.")
            raise exception.InstanceSnapshotContentInvalid(msg)

        if self.size < 1:
            msg = _("Instance snapshot size must be positive integer.")
            raise exception.InstanceSnapshotSizeInvalid(msg)
