# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from falcon import testing
import os, sys
import unittest
from test_entry import TestEntryClass
sys.path.append(os.path.abspath(""))

# class InitTest(testing.TestCase):
    
#     app = main.main()

#     def setUp(self):
#         super(InitTest, self).setUp()

#         # Initialize and return a `falcon.App` instance.
#         self.app = InitTest.app


# class TestMyApp(InitTest):
#     def test_get_status(self):
#         doc = {'status': 'Ok'}

#         result = self.simulate_get('/api/v1/status')
#         self.assertEqual(result.json, doc)
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestEntryClass("test_static_constants"))
    suite.addTest(TestEntryClass("test_parse_uri_default_http"))
    suite.addTest(TestEntryClass("test_parse_uri_default_https"))
    suite.addTest(TestEntryClass("test_parse_uri_default_non_http_https"))
    suite.addTest(TestEntryClass("test_new_entry"))
    suite.addTest(TestEntryClass("test_update_entry_uri"))
    suite.addTest(TestEntryClass("test_validate_id"))
    suite.addTest(TestEntryClass("test_validate_digest"))
    suite.addTest(TestEntryClass("test_validate_datetime"))
    suite.addTest(TestEntryClass("test_manually_set_digest"))
    return suite

if "__main__" == __name__:
    runner = unittest.TextTestRunner()
    runner.run(test_suite())