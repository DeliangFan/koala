#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

import datetime

import pecan
from pecan import rest

from koala.api.controllers.v1 import base
from koala.common import exception
from koala.common.wsmeext import pecan as wsme_pecan
from koala.openstack.common.gettextutils import _
from koala.openstack.common import importutils
from wsme import types as wtypes

REQUIRED_PRICE_PROPERTIES = ('name', 'region', 'resource_type', 'unit_price')
REQUIRED_EVENT_PROPERTIES = ('resource_id', 'resource_type', 'event_type',
                              'event_time', 'region', 'tenant_id', 'content')
RESOURCE_AFFINITY_TYPES = ('instance', 'volume', 'router', 'floating_ip',
                           'instance_snapshot', 'volume_snapshot', 'alarm',
                           'load_balancer', 'image')
RESOURCE_CLASS_MAP = {
    'instance': 'instance.Instance',
    'image': 'image.Image',
    'volume': 'volume.Volume',
    'router': 'router.Router',
    'alarm': 'alarm.Alarm',
    'floating_ip': 'floating_ip.FloatingIP',
    'load_balancer': 'load_balancer.LoadBalancer',
    'volume_snapshot': 'volume_snapshot.VolumeSnapshot',
    'instance_snapshot': 'instance_snapshot.InstanceSnapshot'}


class Price(base.APIBase):
    """The id of the resource price."""
    id = int
    unit_price = float
    name = wtypes.text
    region = wtypes.text
    description = wtypes.text
    # NOTE(fandeliang) we should take care of the volume, ssd or sata
    resource_type = wtypes.text

    @classmethod
    def sample(cls):
        return cls(
            id=1,
            name='disk',
            region='bj',
            unit_price=0.8,
            resource_type='volume',
            description='Price of volume.'
        )


class PricesController(rest.RestController):

    @wsme_pecan.wsexpose(Price, int)
    def get_one(self, id):
        """Get the price by id."""
        prices = pecan.request.dbapi.price_get_by_id(id)
        if not prices:
            msg = _("Price %s not found.") % str(id)
            raise exception.PriceNotFound(msg)

        return prices[0]

    @wsme_pecan.wsexpose([Price])
    def get_all(self):
        """Return all the prices."""
        prices = pecan.request.dbapi.prices_get_all()

        return prices

    @wsme_pecan.wsexpose(Price, body=Price, status_code=201)
    def post(self, data):
        """Create a new price."""
        value = data.as_dict()

        for key in REQUIRED_PRICE_PROPERTIES:
            if key not in value:
                msg = _("Property %s is required by the price.") % key
                raise exception.Invalid(msg)

        id = value.get('id', None)
        if id:
            existed_price = pecan.request.dbapi.price_get_by_id(id)
            if existed_price:
                msg = _("Price %s already exists.") % str(id)
                raise exception.PriceIdConflict(msg)

        """Create the new price."""
        price = pecan.request.dbapi.price_create(value)

        return price

    @wsme_pecan.wsexpose(Price, body=Price)
    def put(self, data):
        """Modify the price."""
        value = data.as_dict()

        id = value.get('id', None)
        if not id:
            msg = _("Property id is required by the price.")
            raise exception.Invalid(msg)
        else:
            existed_price = pecan.request.dbapi.price_get_by_id(id)
            if not existed_price:
                msg = _("Price %s not found.") % str(id)
                raise exception.PriceNotFound(msg)

        price = pecan.request.dbapi.price_update_by_id(id, value)

        return price

    @wsme_pecan.wsexpose(None, int, status_code=204)
    def delete(self, id):
        """Delete the price by id."""
        prices = pecan.request.dbapi.price_get_by_id(id)
        if not prices:
            msg = _("Price %s not found.") % str(id)
            raise exception.PriceNotFound(msg)

        pecan.request.dbapi.price_delete_by_id(id)


class Resource(base.APIBase):
    "The consumption of resource."
    resource_id = wtypes.text
    resource_name = wtypes.text
    status = wtypes.text
    region = wtypes.text
    consumption = float
    deleted = int
    tenant_id = wtypes.text
    resource_type = wtypes.text
    created_at = datetime.datetime
    updated_at = datetime.datetime
    deleted_at = datetime.datetime
    description = wtypes.text

    @classmethod
    def sample(cls):
        return cls(
            resource_id='ea75b3e1-e3b6-4777-bc4e-ef6ea414ace2',
            resource_name='volume01',
            status='in-use',
            region='bj',
            consumption=23.56,
            deleted=0,
            tenant_id='7f13f2b17917463b9ee21aa92c4b36d6',
            resource_type='volume',
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
            deleted_at=None,
            description='The resource consumption.'
        )


class ResourcesController(rest.RestController):
    """Resources controller.

    Resource keeps the global information for a billing resource. Only when
    koala recieve an event from ceilometer, than it will generate a new
    resource or update the existed resource. So it is only necessary to expose
    the query APIs.
    """

    @wsme_pecan.wsexpose(Resource, wtypes.text)
    def get_one(self, resource_id):
        """Get the resource information by id."""
        resources = pecan.request.dbapi.resource_get_by_id(resource_id)
        if not resources:
            msg = _("Resource %s not found.") % resource_id
            raise exception.ResourceNotFound(msg)

        return resources[0]

    @wsme_pecan.wsexpose([Resource])
    def get_all(self):
        """Return all the resources."""
        # TBD(fandeliang) supports to query resources.
        # query with limits
        # query by tenant_id
        resources = pecan.request.dbapi.resources_get_all()

        return resources


class Record(base.APIBase):
    "The consumption of resource."
    resource_id = wtypes.text
    consumption = float
    unit_price = float
    start_at = datetime.datetime
    end_at = datetime.datetime
    description = wtypes.text

    @classmethod
    def sample(cls):
        start_time = datetime.datetime.utcnow()

        return cls(
            resource_id='ea75b3e1-e3b6-4777-bc4e-ef6ea414ace2',
            consumption=0.8,
            unit_price=0.8,
            start_at=start_time,
            end_at=start_time.replace(hour=start_time.hour + 1),
            description='Hourly billing.'
        )


class RecordsController(rest.RestController):
    """Records controller.

    Record keeps the hourly billing records for the resource. Only when koala
    recieve an event from ceilometer, than it will generate a new records. So
    it is only necessary to expose the query API.
    """
    # TBD(fandeliang) should implement get_all?

    @wsme_pecan.wsexpose([Record], wtypes.text)
    def get_one(self, resource_id):
        """In fact, we will list all the records by resource_id."""
        records = pecan.request.dbapi.records_get_by_resource_id(resource_id)
        if not records:
            msg = _("Records of resource %s not found.") % resource_id
            raise exception.RecordNotFound(msg)

        return records


class Content(base.APIBase):
    # Instance content.
    vcpu = int
    ram = int
    disk = int
    flavor = wtypes.text
    # Volume, volume snapshot, image and instance snapshot content.
    size = int
    # Floating IP content, you can billing floating IP by bandwidth or traffic.
    bandwidth = int
    traffic = int

    @classmethod
    def sample(cls):
        return cls(
            vcpu=2,
            ram=4096,
            disk=20
        )


class Event(base.APIBase):
    "The event recieved from ceilometer."
    resource_id = wtypes.text
    resource_name = wtypes.text
    resource_type = wtypes.text
    event_type = wtypes.text
    event_time = datetime.datetime
    tenant_id = wtypes.text
    region = wtypes.text
    # Different resources have different content, for instance,
    # the content contains information of vcpu, ram and disk.
    content = Content

    @classmethod
    def sample(cls):
        return cls(
            resource_id='ea75b3e1-e3b6-4777-bc4e-ef6ea414ace2',
            resource_name='volume01',
            resource_type='volume',
            event_type='create',
            event_time=datetime.datetime.utcnow(),
            tenant_id='7f13f2b17917463b9ee21aa92c4b36d6',
            region='bj',
            content={'size': 10}
        )


class EventsController(rest.RestController):
    """Recieve events from ceilometer.

       Once a new event comes, we will analyse it and generate the
       billing record and store the result to database.

       Note: we only need to expose post API.
    """

    # NOTE(fandeliang) should we implement events API which is able
    # to recieve event list.
    # And how to implement the API?

    def check_event_data(self, data):
        value = data.as_dict()

        for key in REQUIRED_EVENT_PROPERTIES:
            if key not in value:
                msg = _("Property %s is required by the event.") % key
                raise exception.Invalid(msg)

        if value['resource_type'] not in RESOURCE_AFFINITY_TYPES:
            msg = _("Resource type must be in %s") % str(
                REQUIRED_EVENT_PROPERTIES)
            raise exception.ResourceTypeInvalid(msg)

        return value

    def init_resource(self, value):
        path = 'koala.billing.' + RESOURCE_CLASS_MAP[value.get(
            'resource_type')]
        resource = importutils.import_object(path, value)

        return resource

    @wsme_pecan.wsexpose(None, body=Event, status_code=204)
    def post(self, data):
        """Check the recieved event carefully and then use it for billing."""

        value = self.check_event_data(data)
        resource = self.init_resource(value)
        resource.billing_resource()


class Controller(object):
    """Version 1 API controller root."""

    prices = PricesController()
    resources = ResourcesController()
    records = RecordsController()
    events = EventsController()
