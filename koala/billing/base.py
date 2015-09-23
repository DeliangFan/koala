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

from koala.common import exception
from koala.db.sqlalchemy import api as dbapi
from koala.openstack.common.gettextutils import _
from koala.openstack.common import jsonutils


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
        self.check_event_type()

    def check_content(self):
        """Check content base on different resource."""

        msg = _("Check content has not been implemented.")
        raise NotImplementedError(msg)

    def check_event_type(self):
        """Check the event type."""

        if self.event_type not in self.EVENT_TYPES:
            msg = _("%(res_type)s event type must be in %(format)s.") % {
                                        'res_type': self.resource_type,
                                        'format': str(self.EVENT_TYPES)}
            raise exception.EventTypeInvalid(msg)

    def get_price(self):
        """Get the resource type by resource type and region."""
        price = self.db_api.price_get_by_resource(self.resource_type,
                                                    self.region)

        if not price:
            msg = _("Price of %(res_type)s in region %(region)s could not "
                    "be found.") % {'res_type': self.resource_type,
                                    'region': self.region}
            raise exception.PriceNotFound(msg)

        return price.unit_price

    def get_resource(self):
        """Get resource from database."""

        resources = self.db_api.resource_get_by_id(self.resource_id)
        if resources:
            resource = resources[0]
            if resource.deleted:
                msg = _("Resource %s has been deleted.") % self.resource_id
                raise exception.ResourceDeleted(msg)
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

        # Convert json to string.
        res['content'] = jsonutils.dumps(self.content)

        description = "Start billing " + self.resource_type
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

    def get_last_record(self):
        """Get the last record of the resource."""
        record = self.db_api.record_get_by_last(self.resource_id)

        return record

    def create_record(self, value):
        """Create a new record of the resource."""

        if 'resource_id' not in value:
            value['resource_id'] = self.resource_id

        if 'end_at' not in value:
            value['end_at'] = self.event_time

        # Unit_price, consumption and description is not easye to get from
        # db, so it must be calculate carefully in each resource.
        for key in ('unit_price', 'consumption', 'description', 'start_at'):
            if key not in value:
                msg = _("Property %s is needed to generate record.")
                raise exception.RecordValueInvalid(msg)

        self.db_api.record_create(value)

    def get_start_at(self):
        """Get the start billing time."""
        last_record = self.get_last_record()

        # If the record is None, it means this is the second event for the
        # resource, so we need the get the start time from resource.
        if not last_record:
            resource = self.get_resource()
            start_at = resource.created_at
        else:
            start_at = last_record.end_at

        if start_at >= self.event_time:
            msg = _("Event time means that it's a privious event.")
            raise exception.EventTimeInvalid(msg)

        return start_at

    def billing_resource(self):
        """Billing the resource and generate billing records.

           This is the mainly function for billing a resource. When the new
           event comes, we check whether the resource is a new or not. If
           it's a new resource, we need to generate a resource corresponding,
           otherwise, we just to calculate the consumption and update the
           billing records.
        """
        if self.get_resource():
            self.calculate_consumption()
        else:
            # NOTE(fandeliang) we still need to check the event type. if the
            # event type is not create, it means that some messages ahead
            # have lost.
            if self.event_type == 'create':
                self.create_resource()
            elif self.event_type == 'delete':
                # If we recieve a delete event with not resource records, just
                # ignore it.
                # TBD(fandeliang) Log.warning(_("Messaging missing"))
                pass
            else:
                # If we recieve a resize or exists event, create the new
                # resource and treat it as the create time.
                # TBD(fandeliang) Log.warning(_("Messaging missing"))
                self.create_resource()
