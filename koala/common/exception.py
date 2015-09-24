# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
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

from koala.openstack.common.gettextutils import _
from koala.openstack.common import log as logging

from oslo.config import cfg

LOG = logging.getLogger(__name__)

exc_log_opts = [
    cfg.BoolOpt('fatal_exception_format_errors',
                default=False,
                help='make exception message format errors fatal'),
]

CONF = cfg.CONF
CONF.register_opts(exc_log_opts)


class KoalaException(Exception):
    """Base Koala Exception

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.

    """
    message = _("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.message % kwargs

            except Exception as e:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception(_('Exception in string format operation'))
                for name, value in kwargs.iteritems():
                    LOG.error("%s: %s" % (name, value))

                if CONF.fatal_exception_format_errors:
                    raise e
                else:
                    # at least get the core message out if something happened
                    message = self.message

        super(KoalaException, self).__init__(message)

    def format_message(self):
        if self.__class__.__name__.endswith('_Remote'):
            return self.args[0]
        else:
            return unicode(self)


class NotAuthorized(KoalaException):
    message = _("Not authorized.")
    code = 403


class Invalid(KoalaException):
    message = _("Unacceptable parameters.")
    code = 400


class NotFound(KoalaException):
    message = _("Resource could not be found.")
    code = 404


class PriceNotFound(NotFound):
    message = _("Price %(id)s could not be found.")


class PriceIdConflict(KoalaException):
    message = _("Price %(id)s conflict with already existed price.")
    code = 409


class ResourceNotFound(NotFound):
    message = _("Resource %(id)s could not be found.")


class ResourceTypeInvalid(Invalid):
    message = _("Invalid Resource type.")


class ResourceDeleted(Invalid):
    message = _("Resource has been deleted.")


class RecordNotFound(NotFound):
    message = _("Records of resource %(id)s could not be found.")


class RecordValueInvalid(NotFound):
    message = _("Invalid value to generate record.")


class EventTypeInvalid(Invalid):
    message = _("Invalid event type.")


class EventDuplicate(Invalid):
    message = _("Duplicate event message.")


class EventTimeInvalid(Invalid):
    message = _("Invalid event time.")


class ImageContentInvalid(Invalid):
    message = _("Image size not specified in the content.")


class ImageSizeInvalid(Invalid):
    message = _("Image size must be positive integer.")


class InstanceSnapshotContentInvalid(Invalid):
    message = _("Instance snapshot size not specified in the content.")


class InstanceSnapshotSizeInvalid(Invalid):
    message = _("Instance snapshot size must be positive integer.")


class InstanceContentInvalid(Invalid):
    message = _("Instance content is invalid.")


class VolumeContentInvalid(Invalid):
    message = _("Invalid volume content.")


class VolumeSizeInvalid(Invalid):
    message = _("Volume size must be positive integer.")


class VolumeSnapshotContentInvalid(Invalid):
    message = _("Invalid volume snapshot content.")


class VolumeSnapshotSizeInvalid(Invalid):
    message = _("Volume snapshot size must be positive integer.")


class RouterContentInvalid(Invalid):
    message = _("Router content should be empty.")
