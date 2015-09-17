#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from koala.api.controllers.v1 import ex


class Controller(object):
    """Version 1 API controller root."""

    exs = ex.ExController()
