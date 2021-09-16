# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest
import os, sys
sys.path.append(os.path.abspath(""))
from entry import Entry
from datetime import datetime
from urllib.parse import SplitResult
import secrets


class TestEntryClass(unittest.TestCase):

    def setUp(self):
        self.default_scheme = Entry.DEFAULT_SCHEME
    
    def tearDown(self):
        Entry.DEFAULT_SCHEME = self.default_scheme

    def test_static_constants(self):
        self.assertEqual(12, Entry.ID_CHAR_MAXLEN, "DB schema allow max 12 chars ID.")
        self.assertEqual(256 / 8, Entry.SHA256_BYTE_LEN, "SHA256 must be 32 bytes in length.")
        self.assertIsNotNone(Entry.DEFAULT_SCHEME, "Default scheme cannot be None")
        self.assertIsNot("", Entry.DEFAULT_SCHEME.strip(), "Default scheme cannot be an empty string")

    def test_parse_uri_default_https(self):
        # SplitResult(scheme, netloc, path, query, fragment)
        Entry.DEFAULT_SCHEME = "https"
        args = {"https://example.com/":
                SplitResult("https", "example.com", "/", "", ""),
                "https://example.com?ex=exp":
                SplitResult("https", "example.com", "", "ex=exp", ""),
                "https://example.com#ex": 
                SplitResult("https", "example.com", "", "", "ex"),
                "https://example.com?ex=exp#123":
                SplitResult("https", "example.com", "", "ex=exp", "123"),
                "https://example.com/?ex=exp#123":
                SplitResult("https", "example.com", "/", "ex=exp", "123"),
                "https://example.com/example":
                SplitResult("https", "example.com", "/example", "", ""),
                "https://example.com/example?ex=exp":
                SplitResult("https", "example.com", "/example", "ex=exp", ""),
                "https://example.com/example#ex":
                SplitResult("https", "example.com", "/example", "", "ex"),
                "https://example.com/example?ex=exp&aa=a#123":
                SplitResult("https", "example.com", "/example", "ex=exp&aa=a", "123"),

                # No scheme
                "example.com":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "", ""),
                "example.com/":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/", "", ""),
                "example.com?ex=exp":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "ex=exp", ""),
                "example.com#ex":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "", "ex"),
                "example.com?ex=exp#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "ex=exp", "123"),
                "example.com/?ex=exp#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/", "ex=exp", "123"),
                "example.com/example":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "", ""),
                "example.com/example?ex=exp":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "ex=exp", ""),
                "example.com/example#ex":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "", "ex"),
                "example.com/example?ex=exp&as=sf#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "ex=exp&as=sf", "123"),
                
                "//example.com/":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/", "", ""),
                "//example.com?ex=exp":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "ex=exp", ""),
                "//example.com#ex":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "", "ex"),
                "//example.com?ex=exp#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "ex=exp", "123"),
                "//example.com/example":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "", ""),
                "//example.com/example?ex=exp":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "ex=exp", ""),
                "//example.com/example#ex":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "", "ex"),
                "example.com/example?ex=exp&as=sf#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "ex=exp&as=sf", "123"),
            }

        for key in args.keys():
            with self.subTest():
                expected = args[key]
                result = Entry.parse_uri(key)
                self.assertEqual(expected, result, f"Expected {expected}, got {result}")

    def test_parse_uri_default_http(self):
        # SplitResult(scheme, netloc, path, query, fragment)
        Entry.DEFAULT_SCHEME = "http"
        args = {"https://example.com/":
                SplitResult("https", "example.com", "/", "", ""),
                "https://example.com?ex=exp":
                SplitResult("https", "example.com", "", "ex=exp", ""),
                "https://example.com#ex": 
                SplitResult("https", "example.com", "", "", "ex"),
                "https://example.com?ex=exp#123":
                SplitResult("https", "example.com", "", "ex=exp", "123"),
                "https://example.com/?ex=exp#123":
                SplitResult("https", "example.com", "/", "ex=exp", "123"),
                "https://example.com/example":
                SplitResult("https", "example.com", "/example", "", ""),
                "https://example.com/example?ex=exp":
                SplitResult("https", "example.com", "/example", "ex=exp", ""),
                "https://example.com/example#ex":
                SplitResult("https", "example.com", "/example", "", "ex"),
                "https://example.com/example?ex=exp&aa=a#123":
                SplitResult("https", "example.com", "/example", "ex=exp&aa=a", "123"),

                # No scheme
                "example.com":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "", ""),
                "example.com/":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/", "", ""),
                "example.com?ex=exp":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "ex=exp", ""),
                "example.com#ex":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "", "ex"),
                "example.com?ex=exp#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "ex=exp", "123"),
                "example.com/?ex=exp#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/", "ex=exp", "123"),
                "example.com/example":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "", ""),
                "example.com/example?ex=exp":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "ex=exp", ""),
                "example.com/example#ex":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "", "ex"),
                "example.com/example?ex=exp&as=sf#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "ex=exp&as=sf", "123"),
                
                "//example.com/":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/", "", ""),
                "//example.com?ex=exp":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "ex=exp", ""),
                "//example.com#ex":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "", "ex"),
                "//example.com?ex=exp#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "", "ex=exp", "123"),
                "//example.com/example":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "", ""),
                "//example.com/example?ex=exp":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "ex=exp", ""),
                "//example.com/example#ex":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "", "ex"),
                "example.com/example?ex=exp&as=sf#123":
                SplitResult(Entry.DEFAULT_SCHEME, "example.com", "/example", "ex=exp&as=sf", "123"),
        }

        for key in args.keys():
            with self.subTest():
                expected = args[key]
                result = Entry.parse_uri(key)
                self.assertEqual(expected, result, f"Expected {expected}, got {result}")

    def test_parse_uri_default_non_http_https(self):
        # SplitResult(scheme, netloc, path, query, fragment)
        args = [(
                   "0x5d67690768F0Fc4780c578393Ca567e5bCb38378",
                    SplitResult("ethereum", "", "0x5d67690768F0Fc4780c578393Ca567e5bCb38378", "", ""),
                    "ethereum"
                ), (
                   "0x5d67690768F0Fc4780c578393Ca567e5bCb38378?msg=asdf#123",
                    SplitResult("ethereum", "", "0x5d67690768F0Fc4780c578393Ca567e5bCb38378", "msg=asdf", "123"),
                    "ethereum"
                ),
        ]

        for entry in args:
            with self.subTest():
                Entry.DEFAULT_SCHEME = entry[2]
                expected = entry[1]
                result = Entry.parse_uri(entry[0])
                self.assertEqual(expected, result, f"Expected {expected}, got {result}")

    def test_new_entry(self):
        expected_time = datetime.now()
        dummy_id = "123456"
        args = [(
                    # No scheme
                    "//example.com/example?ex=exp&as=sf#123",                            # Input
                    "https://example.com/example?ex=exp&as=sf#123",                       # Expected URI
                    "https://example.com/example?ex=exp&amp;as=sf#123",                   # Expected HTML safe URI
                    "https://example.com/example?ex=exp&as=sf#123",                       # Expected encoded URI
                    "c276fd410dc58f69d79339d6203db56fd69e57ef2cb2553e2776ab56547175bc",  # Expected URI SHA256
                    (expected_time, expected_time, expected_time, expected_time)         # (init created, init access, expected created, expected access)
                ), (
                    # Non http/https scheme
                    "ethereum:0x5d67690768F0Fc4780c578393Ca567e5bCb38378",
                    "ethereum:0x5d67690768F0Fc4780c578393Ca567e5bCb38378",
                    "ethereum:0x5d67690768F0Fc4780c578393Ca567e5bCb38378",
                    "ethereum:0x5d67690768F0Fc4780c578393Ca567e5bCb38378",
                    "6efd3b5e0c3b9cfea2a61718a4e814852ac0f150dfb26246632e743a811d9587",
                    (expected_time, expected_time, expected_time, expected_time)
                ), (
                    # Non ascii chars in domain (netloc), path, query and fragment
                    "例子.com/例子?例子=例子#例子",
                    "https://例子.com/例子?例子=例子#例子",
                    "https://例子.com/例子?例子=例子#例子",
                    "https://xn--fsqu00a.com/%E4%BE%8B%E5%AD%90?%E4%BE%8B%E5%AD%90=%E4%BE%8B%E5%AD%90#%E4%BE%8B%E5%AD%90",
                    "614d53494396d1991d106ccdd3a255dc672a843a1732c6ee5acdd62f9cb415bf",
                    (None, expected_time, None, expected_time)
                ), (
                    # XSS 1
                    "http://example.com/<script>alert(1)</script>?<script>alert(1)</script>=<script>alert(1)</script>&<script>alert(1)</script>=<script>alert(1)</script>#<script>alert(1)</script>",
                    "http://example.com/<script>alert(1)</script>?<script>alert(1)</script>=<script>alert(1)</script>&<script>alert(1)</script>=<script>alert(1)</script>#<script>alert(1)</script>",
                    "http://example.com/&lt;script&gt;alert(1)&lt;/script&gt;?&lt;script&gt;alert(1)&lt;/script&gt;=&lt;script&gt;alert(1)&lt;/script&gt;&amp;&lt;script&gt;alert(1)&lt;/script&gt;=&lt;script&gt;alert(1)&lt;/script&gt;#&lt;script&gt;alert(1)&lt;/script&gt;",
                    "http://example.com/%3Cscript%3Ealert(1)%3C/script%3E?%3Cscript%3Ealert(1)%3C/script%3E=%3Cscript%3Ealert(1)%3C/script%3E&%3Cscript%3Ealert(1)%3C/script%3E=%3Cscript%3Ealert(1)%3C/script%3E#%3Cscript%3Ealert(1)%3C/script%3E",
                    "5d8ed23944fbc66b7596501245d87aaa567cfd67e6773b46c306f06c75b63572",
                    (expected_time, None, expected_time, None)
                ), (
                    # + in path should not be encoded
                    "https://example.com/?q=test+123",
                    "https://example.com/?q=test+123",
                    "https://example.com/?q=test+123",
                    "https://example.com/?q=test+123",
                    "b9ea5b134f4d87fc44ed739dda4babc1ae6aecbd20849e649c3f6b2a7111c0b1",
                    (None, None, None, None)
                ), (
                    # XSS 2
                    "<script>alert(1)</script>://<script>alert(1)</script>",
                    "https://<script>alert(1)</script>://<script>alert(1)</script>",
                    "https://&lt;script&gt;alert(1)&lt;/script&gt;://&lt;script&gt;alert(1)&lt;/script&gt;",
                    "https://<script>alert(1)</script%3E://%3Cscript%3Ealert(1)%3C/script%3E",
                    "4fec1a8e8efc07e333a1cec9c8e5364e9fc53eb659a226b18200186539374a04",
                    (None, None, None, None)
                ), (
                    # bleach will treat "<something" as invalid tag and will remove it
                    "https://example.com/<dontremoveme",
                    "https://example.com/<dontremoveme",
                    "https://example.com/&lt;dontremoveme",
                    "https://example.com/%3Cdontremoveme",
                    "ee604c00b2433ed6e2381c7f5fe0e09462c8f9445de67cc0ff07fccfc11d80fa",
                    (None, None, None, None)
                ), (
                    "example.com/?><dontremoveme=<<eot",
                    "https://example.com/?><dontremoveme=<<eot",
                    "https://example.com/?&gt;&lt;dontremoveme=&lt;&lt;eot",
                    "https://example.com/?%3E%3Cdontremoveme=%3C%3Ceot",
                    "545a13b6f6b017e0a62915f2a0458b45e711d0a9340d37b2daad2fabb19e58ea",
                    (None, None, None, None)
                ), (
                    # mailto URI
                    "mailto:John Doe<john_doe@example.com>?subject=Test123%20!@",
                    "mailto:John Doe<john_doe@example.com>?subject=Test123%20!@",
                    "mailto:John Doe&lt;john_doe@example.com&gt;?subject=Test123%20!@",
                    "mailto:John%20Doe%3Cjohn_doe@example.com%3E?subject=Test123%20!@",
                    "e9682458578709dae35fde0ff669c3247943254691e3cb00d59e51983739c595",
                    (expected_time, expected_time, expected_time, expected_time)
                ), (
                    # IPv4 addresses
                    "ssh://test@127.0.0.1:22",
                    "ssh://test@127.0.0.1:22",
                    "ssh://test@127.0.0.1:22",
                    "ssh://test@127.0.0.1:22",
                    "dffc746b578d185807beb500928e3ea27d12b0232e14251286a2eeb0b3270466",
                    (expected_time, expected_time, expected_time, expected_time)
                ), (
                    # IPv6 addresses
                    "ssh://test@[::1]:22",
                    "ssh://test@[::1]:22",
                    "ssh://test@[::1]:22",
                    "ssh://test@[::1]:22",
                    "ca1c3df3eb6ab106f10652ddd862081e8c2a19cdbf0acb9dc146640c500954f7",
                    (expected_time, expected_time, expected_time, expected_time)
                ),
        ]
        for entry in args:
            with self.subTest():
                input_uri = entry[0]
                created_time = entry[5][0]
                accessed_time = entry[5][1]
                result = Entry(dummy_id, input_uri, created_time, accessed_time)
                expected_uri = entry[1]
                expected_safe = entry[2]
                expected_encoded = entry[3]
                expected_sha256 = entry[4]
                expected_created_on = entry[5][2]
                expected_last_accessed = entry[5][3]
                
                self.assertEqual(dummy_id, result.id, "Unexpected ID.")
                self.assertEqual(expected_uri, result.uri, "Unexpected URI.")
                self.assertEqual(expected_safe, result.html_safe_uri, "Unexpected HTML safe URI.")
                self.assertEqual(expected_encoded, result.encoded_uri, "Unexpected encoded URI.")
                self.assertEqual(expected_sha256, result.get_sha256(), "Unexpected SHA256 of URI.")
                self.assertEqual(expected_created_on, result.created_on, "Unexpected Created On value.")
                self.assertEqual(expected_last_accessed, result.last_accessed, "Unexpected Last Accessed value.")

    def test_update_entry_uri(self):
        dummy_id = "akjsef"
        args = [(
                    # No scheme
                    "//example.com/example?ex=exp&as=sf#123",                           # Original
                    "example.com/asdf",                                                 # Update to
                    "https://example.com/asdf",                                          # Expected URI
                    "https://example.com/asdf",                                          # Expected HTML safe URI
                    "https://example.com/asdf",                                          # Expected encoded URI
                    "123f83be5cb160bbddfae91c03fad508bf96a6cdd4a1cd74cc4105504bdd7120"  # Expected URI SHA256
                ), (
                    # Non http/https scheme
                    "ethereum:0x5d67690768F0Fc4780c578393Ca567e5bCb38378",
                    "bitcoin:bc1qww8sktvenl044juafgvt068yah9dxuwrhht4kq",
                    "bitcoin:bc1qww8sktvenl044juafgvt068yah9dxuwrhht4kq",
                    "bitcoin:bc1qww8sktvenl044juafgvt068yah9dxuwrhht4kq",
                    "bitcoin:bc1qww8sktvenl044juafgvt068yah9dxuwrhht4kq",
                    "951e655969a5fa76644ad5c207bca282b7873108821eca55fc3bd1f559d20971"
                ), (
                    # Non ascii chars in domain (netloc), path, query and fragment
                    "http://example.com",
                    "例子.com/例子?例子=例子#例子",
                    "https://例子.com/例子?例子=例子#例子",
                    "https://例子.com/例子?例子=例子#例子",
                    "https://xn--fsqu00a.com/%E4%BE%8B%E5%AD%90?%E4%BE%8B%E5%AD%90=%E4%BE%8B%E5%AD%90#%E4%BE%8B%E5%AD%90",
                    "614d53494396d1991d106ccdd3a255dc672a843a1732c6ee5acdd62f9cb415bf"
                )
        ]
        for entry in args:
            with self.subTest():
                result = Entry(dummy_id, entry[0])
                result.update_uri(entry[1])
                expected_uri = entry[2]
                expected_safe = entry[3]
                expected_encoded = entry[4]
                expected_sha256 = entry[5]
                expected_created_on = None
                expected_last_accessed = None
                
                self.assertEqual(dummy_id, result.id, "Unexpected ID.")
                self.assertEqual(expected_uri, result.uri, "Unexpected URI.")
                self.assertEqual(expected_safe, result.html_safe_uri, "Unexpected HTML safe URI.")
                self.assertEqual(expected_encoded, result.encoded_uri, "Unexpected encoded URI.")
                self.assertEqual(expected_sha256, result.get_sha256(), "Unexpected SHA256 of URI.")
                self.assertEqual(expected_created_on, result.created_on, "Unexpected Created On value.")
                self.assertEqual(expected_last_accessed, result.last_accessed, "Unexpected Last Accessed value.")

    @unittest.expectedFailure
    def test_validate_id(self):
        fn = Entry.is_valid_id
        args = [(None, TypeError),
                ("", ValueError),
                (secrets.token_urlsafe(Entry.ID_CHAR_MAXLEN + 1), ValueError)]
        for item in args:
            with self.subTest():
                exception = item[1]
                argument = item[0]
                with self.assertRaises(exception):
                    fn(argument)

    def test_validate_digest(self):
        fn = Entry.is_valid_digest
        args = [(None, TypeError),
                ("951e655969a5fa76644ad5c207bca282b7873108821eca55fc3bd1f559d20971", TypeError),
                (bytes.fromhex("951e655969a5fa76644ad5c207bca282b7873108821eca55fc3bd1f559d20971ffffff"), ValueError),
                (bytes.fromhex("951e6559695fc3bd1f559d20971fffff"), ValueError),
                (bytes.fromhex(""), ValueError),
                (bytearray.fromhex("951e655969a5fa76644ad5c207bca282b7873108821eca55fc3bd1f559d20971ffffff"), ValueError),
                (bytearray.fromhex("951e6559695fc3bd1f559d20971fffff"), ValueError),
                (bytearray.fromhex(""), ValueError),
                ]
        for item in args:
            with self.subTest():
                exception = item[1]
                argument = item[0]
                with self.assertRaises(exception):
                    fn(argument)

        positive_result_1 = bytes.fromhex("951e655969a5fa76644ad5c207bca282b7873108821eca55fc3bd1f559d20971")
        positive_result_2 = bytearray.fromhex("951e655969a5fa76644ad5c207bca282b7873108821eca55fc3bd1f559d20971")
        with self.subTest():
            self.assertEqual(positive_result_1, Entry.is_valid_digest(positive_result_1))
        with self.subTest():
            self.assertEqual(positive_result_2, Entry.is_valid_digest(positive_result_2))

    def test_validate_datetime(self):
        fn = Entry.is_valid_datetime
        args = [(None, TypeError),
                ("Fri 06 Aug 2021 01:06:07 AM GMT", TypeError)]
        for item in args:
            with self.subTest():
                exception = item[1]
                argument = item[0]
                with self.assertRaises(exception):
                    fn(argument)

    def test_manually_set_digest(self):
        original = Entry("asdsdf", "example.com")
        old_digest = original.get_sha256()
        original.set_digest(bytes.fromhex("951e655969a5fa76644ad5c207bca282b7873108821eca55fc3bd1f559d20971"))
        new_digest = original.get_sha256()
        self.assertNotEqual(old_digest, new_digest)
        expected_new = "951e655969a5fa76644ad5c207bca282b7873108821eca55fc3bd1f559d20971"
        self.assertEqual(expected_new, new_digest)
