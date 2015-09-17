# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
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

from koala.tests.api import base


class TestBase(base.FunctionalTest):

    def test_api_setup(self):
        pass

    def test_bad_uri(self):
        response = self.get_json('/bad/path',
                                 expect_errors=True,
                                 headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_int, 404)
        self.assertEqual(response.content_type, "application/json")
