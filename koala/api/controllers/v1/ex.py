import pecan
from pecan import rest

from koala.common.wsmeext import pecan as wsme_pecan
from wsme import types as wtypes


from koala.api.controllers.v1 import base


class Ex(base.APIBase):
    uuid = wtypes.text
    title = wtypes.text
    content = wtypes.text


class ExController(rest.RestController):
    """Version 1 API controller Ex."""

    @wsme_pecan.wsexpose(Ex, unicode, unicode)
    def get_one(self, ex):
        """get a single ex.

        :param ex: uuid or id of the ex
        """
        return pecan.request.dbapi.get_ex(ex)

    @wsme_pecan.wsexpose([Ex], unicode)
    def get_all(self):
        """get all exs

        """
        return pecan.request.dbapi.get_exs()

    @wsme_pecan.wsexpose(Ex, unicode, body=Ex)
    def post(self, ex):
        """Create a new ex

        :param ex: contains ex content
        """

        try:
            new_ex = pecan.request.dbapi.create_ex(ex.as_dict())
            return new_ex
        except Exception:
            raise

    @wsme_pecan.wsexpose(Ex, unicode, unicode, body=Ex)
    def put(self, ex, delta):
        """Update an existing ex.

        :param ex: uuid or id of the ex
        :param delta_ex: dict of new values
        """

        try:
            ex = pecan.request.dbapi.update_ex(ex, delta.as_dict())
            return ex
        except Exception:
            raise

    @wsme_pecan.wsexpose(None, unicode, unicode)
    def delete(self, ex):
        """Delete a ex

        :param ex: uuid or id of the ex
        """
        pecan.request.dbapi.destroy_ex(ex)
