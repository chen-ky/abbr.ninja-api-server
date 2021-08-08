# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import secrets
import string
from mariadb_client import DBClient
import mariadb
from config_parser import ConfigParser as Config
from entry import Entry

class Logic:
    
    CONFUSING_CHARS = ['1', 'l', 'L', 'I', 'i', '0', 'O', 'o']

    def __init__(self):
        self.init_ok = False
        self.maintenance_mode = False
        Config() # Initialise and parse configuration
        config = Config.get_config()
        self.id_chars = config["preference"]["id_char_count"]

        self.charset = string.ascii_letters + string.digits
        if config["preference"]["exclude_confusing_chars"]:
            for char in Logic.CONFUSING_CHARS:
                self.charset = self.charset.replace(char, "")

        self.reserved_path = config["preference"]["reserved_path"]

        # Connect to DB
        user = config["database"]["user"]
        password = config["database"]["password"]
        host = config["database"]["host"]
        port = config["database"]["port"]
        
        # mariadb.OperationalError raised if connection fail
        self.db = DBClient(user, password, host, port)
        
        if config["preference"]["maintenance_mode"]:
            self.maintenance_mode = True
        self.init_ok = True

    def gen_new_id(self, long_uri):
        """
        Returns:
        None: Some error has occurred (Pool of available id running low etc..)
        Entry: Entry instance containing the id
        """
        if not isinstance(long_uri, str):
            raise TypeError(f"\"{long_uri}\" not a string.")
        
        new_entry = Entry("", long_uri, None, None)
        
        # Check for existing entry
        existing_entry = self.db.get_entry_from_digest(new_entry.sha256)
        if len(existing_entry) > 0:
            return existing_entry[0]
        
        new_id = Logic.no_check_gen_id(self.charset, self.id_chars)

        # Check generated id does not exist
        existing_entry = self.db.get_entry_from_id(new_id)
        # Generate new entry until a new one was found, max 50 attempt
        i = 0
        while (len(existing_entry)) > 0 or (new_id in self.reserved_path):
            if i == 50: # Max attempt
                print("WARNING: Cannot generate ID, max attempt reached.")
                return None
            new_id = Logic.no_check_gen_id(self.charset, self.id_chars)
            existing_entry = self.db.get_entry_from_id(new_id)
            i += 1

        new_entry.id = new_id
        self.db.create_new_entry(new_entry)
        return new_entry

    def is_db_up(self):
        if self.db is None:
            return False
        try:
            self.db.ping()
        except mariadb.InterfaceError as e:
            print(f"WARNING: {e}")
            return False
        return True

    @staticmethod
    def no_check_gen_id(charset, id_len):
        return "".join(secrets.choice(charset) for _ in range(id_len))

    def get_uri(self, id):
        result = self.db.get_entry_from_id(id)
        if len(result) < 1:
            return None
        self.db.update_access_date(id)
        return result[0]
