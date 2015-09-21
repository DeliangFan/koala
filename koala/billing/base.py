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

from koala.db.sqlalchemy import api as dbapi
from koala.openstack.common.gettextutils import _


class Resource(object):
    def __init__(self, value):
        """Initiate the resource by event value."""

        self.resource_id = value['resource_id']
        self.resource_type = value['resource_type']
        self.resource_name = value.get('resource_name', None)
        self.event_type = value['event_type']
        self.event_time = value['event_time']
        self.content = value['content'].as_dict()
        self.tenant_id = value['tenant_id']
        self.region = value.get('region', None)

        self.db_api = dbapi.get_backend()

    def check_event_type(self):
        """Check the event type."""

        msg = _("Check event type has not been implemented.")
        raise NotImplementedError(msg)

    def check_content(self):
        """Check content base on different resource."""

        msg = _("Check content has not been implemented.")
        raise NotImplementedError(msg)

    def billing_resource(self):
        """Billing the resource and generate billing records."""

        msg = _("Billing resource has not been implemented.")
        raise NotImplementedError(msg)

    def get_resource(self):
        """Get resource from database."""

        resources = self.db_api.resource_get_by_id(self.resource_id)
        if resources:
            resource = resources[0]
        else:
            resource = None

        return resource

    def create_resource(self):
        res = {}
        res['resource_id'] = self.resource_id
        res['resource_name'] = self.resource_name
        res['region'] = self.region
        res['consumption'] = 0
        res['deleted'] = 0
        res['tenant_id'] = self.tenant_id
        res['resource_type'] = self.resource_type
        res['created_at'] = self.event_time
        
        description = self.resource_type + " has been " + self.event_type
        res['description'] = description

        """Create the new resource."""
        self.resource = self.db_api.resource_create(res)

        return self.resource

    def update_resource(self, value):
        """Update the resource information by resource id.

           We may only want to update the consumption, status, resource_name
           and description information.
        """

        self.db_api.resource_update_by_id(self.resource_id, value)
