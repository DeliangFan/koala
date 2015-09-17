from pecan import rest
from wsmeext import pecan

from koala.api.controllers import v1


class RootController(rest.RestController):

    v1 = v1.Controller()

    @pecan.wsexpose(unicode)
    def get(self):
        return "It works"
