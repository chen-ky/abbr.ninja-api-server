# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
from cryptography.hazmat.primitives import hashes
import bleach
import urllib.parse as urlparser

class Entry:
    
    ID_CHAR_MAXLEN = 12
    SHA256_BYTE_LEN = 32
    DEFAULT_SCHEME = "http"

    def __init__(self, id, uri, created_on=None, last_accessed=None):
        Entry.is_valid_id(id)
        if not created_on is None:
            Entry.is_valid_datetime(created_on)
        if not last_accessed is None:
            Entry.is_valid_datetime(last_accessed)

        self.id = id
        self.uri = None
        self.html_safe_uri = None
        self.encoded_uri = None
        self.sha256 = None # SHA256 of self.uri
        self.update_uri(uri)
        self.created_on = created_on
        self.last_accessed = last_accessed

    def update_uri(self, uri):
        """Update URI and also recalculate checksum."""
        parsed_uri = Entry.parse_uri(uri)
        self.uri = Entry.uri_to_str(parsed_uri)
        self.html_safe_uri = Entry.sanitize_uri(self.uri)
        self.encoded_uri = Entry.uri_to_str(Entry.encode_uri(parsed_uri))
        hash = hashes.Hash(hashes.SHA256())
        hash.update(self.uri.encode())
        self.sha256 = hash.finalize()
        return self

    def set_digest(self, digest):
        """
        This is only intended to be used when retrieving data from database
        Please do not manually modify any digest to prevent inconsistent data
        `update_uri(self, uri)` will update digest automatically when called.
        """
        digest = Entry.is_valid_digest(digest)
        self.sha256 = digest

    def get_sha256(self):
        if self.sha256 is None:
            return None
        Entry.is_valid_digest(self.sha256)
        return self.sha256.hex()

    @staticmethod
    def is_valid_id(id):
        if not isinstance(id, str):
            raise TypeError("Id must be a string type.")
        # elif len(id) == 0:
        #     raise ValueError("ID cannot be an empty string.")
        elif len(id) > Entry.ID_CHAR_MAXLEN:
            raise ValueError(f"ID exceeds max length of {Entry.ID_CHAR_MAXLEN}.")

    @staticmethod
    def is_valid_uri(uri):
        if not isinstance(uri, str):
            raise TypeError("URI must be a string type.")
        uri = uri.strip()
        if uri == "":
            raise ValueError("URI cannot be an empty string.")
        return urlparser.urlsplit(uri)

    @staticmethod
    def is_valid_parsed_uri(parsed_uri):
        if not isinstance(parsed_uri, urlparser.SplitResult):
            raise TypeError("parsed_uri not a SplitResult type.")

    @staticmethod
    def is_valid_digest(sha256):
        if isinstance(sha256, bytearray):
            sha256 = bytes(sha256)
        if not isinstance(sha256, bytes):
            raise TypeError("SHA256 must be a bytes or bytearray type.")
        if len(sha256) != Entry.SHA256_BYTE_LEN:
            raise ValueError(f"SHA256 is not {Entry.SHA256_BYTE_LEN} bytes in length.")
        return sha256

    @staticmethod
    def is_valid_datetime(date):
        if not isinstance(date, datetime.datetime):
            raise TypeError("Not a datetime type.")

    @staticmethod
    def parse_uri(uri_str):
        """
        Parse URI from string, apply DEFAULT_SCHEME if scheme is not specified
        
        Return:
        SplitResult class in urllib.parse
        """
        uri = Entry.is_valid_uri(uri_str)
        if Entry.DEFAULT_SCHEME.lower() in ["http", "https"]: # Scheme normally with netloc populated
            if uri.scheme is None or uri.scheme == "":
                # Parse string like duckduckgo.com to http://duckduckgo.com
                # instead of http:duckduckgo.com
                if uri.netloc is None or uri.netloc == "":
                    uri = uri._replace(netloc=uri.path)
                    uri = uri._replace(path="")
                    uri = urlparser.urlsplit(urlparser.urlunsplit(uri)) # Reparse URI if netloc contains path
                uri = uri._replace(scheme=Entry.DEFAULT_SCHEME)
        else:
            if uri.scheme is None or uri.scheme == "":
                uri = uri._replace(scheme=Entry.DEFAULT_SCHEME)
        return uri

    @staticmethod
    def uri_to_str(parsed_uri):
        Entry.is_valid_parsed_uri(parsed_uri)
        return urlparser.urlunsplit(parsed_uri)

    @staticmethod
    def sanitize_uri(uri_str):
        if not isinstance(uri_str, str):
            raise TypeError("URI must be a string type.")

        # Bleach will clean http://<example.com to http://
        # We want http://&lt;example.com, therefore we replace those
        # chars first before passing it to bleach for further sanitization
        blacklist = [("<", "&lt;"), (">", "&gt;")]
        for target, replacement in blacklist:
            uri_str = uri_str.replace(target, replacement)
        return bleach.clean(uri_str)

    @staticmethod
    def encode_uri(parsed_uri):
        """
        Encode URI, where:
        "netloc" is encoded with idna
        "path", "query" and "fragment" are percent encoded
        
        The result is intended to be used in the "Location" header for 301 redirects.
        """
        Entry.is_valid_parsed_uri(parsed_uri)
        if not parsed_uri.netloc is None:
            parsed_uri = parsed_uri._replace(netloc=parsed_uri.netloc.encode("idna").decode("utf8"))
        if not parsed_uri.path is None:
            # Safe symbols manually tested by inserting into Firefox address bar, not an ideal list
            parsed_uri = parsed_uri._replace(path=urlparser.quote(parsed_uri.path, safe="-._~:/[]@!$()*+,;%=|\\?&#"))
        if not parsed_uri.query is None:
            parsed_uri = parsed_uri._replace(query=urlparser.quote(parsed_uri.query, safe="-._~:/?[]@!$()*+,;%=&#^|`\\{}"))
        if not parsed_uri.fragment is None:
            parsed_uri = parsed_uri._replace(fragment=urlparser.quote(parsed_uri.fragment, safe="-._~:/?[]@!$()*+,;%=&#^|'\\{}"))
        return parsed_uri

    def __str__(self):
        display = f"ID\t\t: {self.id}\n"
        display += f"URI\t\t: {self.uri}\n"
        display += f"SHA256\t\t: {self.get_sha256()}\n"
        display += f"Created On\t: {self.created_on}\n"
        display += f"Last Accessed\t: {self.last_accessed}"
        return display
