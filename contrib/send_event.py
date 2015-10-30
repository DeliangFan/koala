import datetime
import eventlet
import json
import requests

from ceilometer.openstack.common import log
from ceilometer.openstack.common import timeutils

LOG = log.getLogger(__name__)

RESOURCES_MAP = {'compute': 'instance',
                 'volume': 'volume',
                 'snapshot': 'volume_snapshot',
                 'image': 'image',
                 'router': 'router',
                 'floatingip': 'floating_ip'}

# (NOTE)fandeliang Take carefully of resize.
# We tree revert as resize event.
INSTANCE_EVENT_TYPES_MAP = {
    'create.end': 'create',
    'delete.start': 'delete',
    'power_off.start': 'power_off',
    'power_on.end': 'power_on',
    'shutdown.start': 'power_off',
    'resize.end': 'resize',
    'revert.end': 'resize',
    'exists': 'exists'}

IMAGE_EVENT_TYPES_MAP = {
    'image.upload': 'upload',
    'image.delete': 'delete',
    'image.exists': 'exists'}

VOLUME_EVENT_TYPES_MAP = {
    'create.end': 'create',
    'delete.start': 'delete',
    'resize.end': 'resize',
    'exists': 'exists'}

VOLUME_SNAPSHOT_EVENT_TYPES_MAP = {
    'create.end': 'create',
    'delete.start': 'delete',
    'exists': 'exists'}

ROUTER_EVENT_TYPES_MAP = {
    'create.end': 'create',
    'delete.start': 'delete',
    'exists': 'exists'}

FLOATINGIP_EVENT_TYPES_MAP = {
    'create.end': 'create',
    'delete.start': 'delete',
    'update.end': 'update',
    'exists': 'exists'}


class Message(object):
    def __init__(self, body):
        self.body = body
        self.payload = body.get('payload', {})
        self.msg_event_type = body.get('event_type', '')
        self.event_time = self.extract_when(body)

        self.drop_message = False

    def extract_when(self, body):
        """
        Extract the generated datetime from the notification.
        """
        # NOTE: I am keeping the logic the same as it was in the collector,
        # However, *ALL* notifications should have a 'timestamp' field, it's
        # part of the notification envelope spec. If this was put here because
        # some openstack project is generating notifications without a
        # timestamp, then that needs to be filed as a bug with the offending
        # project (mdragon)

        when = body.get('timestamp', body.get('_context_timestamp'))
        if when:
            # NOTE(fandeliang) LOG.warn()
            return timeutils.normalize_time(timeutils.parse_isotime(when))

        return timeutils.utcnow()

    def filter_message_by_resource_type(self):
        """Filter the message by resource type."""
        self.resource_type = None

        for key in RESOURCES_MAP.keys():
            if key in self.msg_event_type:
                self.resource_type = RESOURCES_MAP[key]

        if not self.resource_type:
            self.drop_message = True

    def filter_message_by_event_type(self):
        """Filter the message by event type."""
        if self.resource_type == 'instance':
            self.filter_instance_message()
        elif self.resource_type == 'image':
            self.filter_image_message()
        elif self.resource_type == 'volume':
            self.filter_volume_message()
        elif self.resource_type == 'router':
            self.filter_router_message()
        elif self.resource_type == 'floating_ip':
            self.filter_floatingip_message()
        elif self.resource_type == 'volume_snapshot':
            self.filter_volume_snapshot_message()

    def filter_instance_message(self):
        """Filter the instance message."""
        self.event_type = None

        for key in INSTANCE_EVENT_TYPES_MAP.keys():
            if key in self.msg_event_type:
                self.event_type = INSTANCE_EVENT_TYPES_MAP[key]

        if not self.event_type:
            self.drop_message = True

        if not self.payload:
            self.drop_message = True
        else:
            self.resource_id = self.payload.get('instance_id')
            self.resource_name = self.payload.get('display_name', None)
            self.tenant_id = self.payload.get('tenant_id')

            disk = self.payload['disk_gb']
            ram = self.payload['memory_mb']
            vcpu = self.payload['vcpus']
            self.content = {'vcpu': vcpu, 'ram': ram, 'disk': disk}

    def filter_image_message(self):
        """Filter the instance message."""
        self.event_type = None

        for key in IMAGE_EVENT_TYPES_MAP.keys():
            if key in self.msg_event_type:
                self.event_type = IMAGE_EVENT_TYPES_MAP[key]

        if not self.event_type:
            self.drop_message = True

        if not self.payload:
            self.drop_message = True
        else:
            self.resource_id = self.payload['id']
            self.resource_name = self.payload.get('name', None)
            self.tenant_id = self.payload['owner']
            self.content = {'size': self.payload['size']}

            is_public = self.payload.get('is_public', False)
            if is_public:
                self.drop_message = True

            image_type = self.payload.get('image_type', False)
            if image_type and image_type == 'snapshot':
                self.resource_type = 'instance_snapshot'

    def filter_volume_message(self):
        """Filter the volume message."""
        self.event_type = None
        for key in VOLUME_EVENT_TYPES_MAP.keys():
            if key in self.msg_event_type:
                self.event_type = VOLUME_EVENT_TYPES_MAP[key]

        if not self.event_type:
            self.drop_message = True

        if not self.payload:
            self.drop_message = True
        else:
            self.resource_id = self.payload['volume_id']
            self.resource_name = self.payload.get('display_name', None)
            self.tenant_id = self.payload['tenant_id']
            self.content = {'size': self.payload['size']}

    def filter_volume_snapshot_message(self):
        """Filter volume snapshot message."""
        self.event_type = None
        for key in VOLUME_SNAPSHOT_EVENT_TYPES_MAP.keys():
            if key in self.msg_event_type:
                self.event_type = VOLUME_SNAPSHOT_EVENT_TYPES_MAP[key]

        if not self.event_type:
            self.drop_message = True

        if not self.payload:
            self.drop_message = True
        else:
            self.resource_id = self.payload['snapshot_id']
            self.resource_name = self.payload.get('display_name', None)
            self.tenant_id = self.payload['tenant_id']
            self.content = {'size': self.payload['volume_size']}

    def filter_router_message(self):
        """Filter router message."""
        self.event_type = None
        for key in ROUTER_EVENT_TYPES_MAP.keys():
            if key in self.msg_event_type:
                self.event_type = ROUTER_EVENT_TYPES_MAP[key]

        if not self.event_type:
            self.drop_message = True
            return None

        # NOTE(fandeliang) fuck the router!
        if not self.payload:
            self.drop_message = True
        else:
            if self.event_type == 'create':
                router = self.payload.get('router', {})
                self.resource_id = router.get('id', None)
                self.resource_name = router.get('name', None)
                self.tenant_id = router.get('tenant_id', None)
                if not self.tenant_id:
                    self.tenant_id = self.body.get('_context_tenant_id')
            elif self.event_type == 'delete':
                self.resource_id = self.payload.get('router_id')
                self.resource_name = self.payload.get('name', None)
                self.tenant_id = self.body.get('_context_tenant_id')

            self.content = {}

        if not self.resource_id:
            self.drop_message = True

    def filter_floatingip_message(self):
        self.drop_message = True

    def send(self):
        # Send the message to koala.
        self.filter_message_by_resource_type()
        self.filter_message_by_event_type()
        self.region = 'bj'

        if self.drop_message:
            LOG.warning(_("Drop message %s.") % self.msg_event_type)
            return None

        url = 'http://127.0.0.1:9999/v1/events'
        headers = {'content-type': 'application/json'}
        body = {
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'resource_type': self.resource_type,
            'event_time': self.event_time.__str__(),
            'event_type': self.event_type,
            'tenant_id': self.tenant_id,
            'region': self.region,
            'content': self.content}

        self.res = requests.post(url, data=json.dumps(body), headers=headers)

        if self.res.status_code not in (200, 201, 202, 204):
            LOG.error(self.res.text)
