# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import mariadb
from entry import Entry

HIGHEST_PORT = pow(2, 16) - 1
DATABASE_NAME = "uri_shortener"

class DBClient:
    
    def __init__(self, user, password, host="::1", port=3306):
        if not isinstance(user, str):
            raise TypeError("Username must be a string type.")
        elif not isinstance(password, str):
            raise TypeError("Password must be a string type.")
        elif not isinstance(host, str):
            raise TypeError("Host must be a string type.")
        elif not isinstance(port, int):
            raise TypeError("Host must be an integer type.")
        
        if port < 0 or port > HIGHEST_PORT:
            raise TypeError(
                f"Port number must be between 0 and {HIGHEST_PORT} inclusive.")
        
        self.connection = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=DATABASE_NAME,
            connect_timeout=5, # TODO Throw this into config
        )
        self.connection.auto_reconnect = True # TODO Config?

        cursor = self.get_cursor()
        # Initialise table if does not exist
        cursor.execute(
            "SHOW TABLES WHERE Tables_in_uri_shortener=?",
            ("uri",))
        if len(cursor.fetchall()) < 1:
            self.create_table()
        cursor.close()

    def get_cursor(self):
        return self.connection.cursor()

    def create_table(self):
        """
        | id (Unique) | original_uri | sha256 | created_on | last_accessed |
        """
        cmd = f"CREATE TABLE uri (\
            id VARCHAR({Entry.ID_CHAR_MAXLEN}) NOT NULL UNIQUE PRIMARY KEY,\
            original_uri TEXT NOT NULL,\
            sha256 BINARY({Entry.SHA256_BYTE_LEN}) NOT NULL,\
            created_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\
            last_accessed DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,\
            INDEX(sha256))"
        cursor = self.get_cursor()
        cursor.execute(cmd)
        self.connection.commit()
        cursor.close()
    
    def create_new_entry(self, entry):
        if not isinstance(entry, Entry):
            raise TypeError("Not an Entry type.")
        cmd = "INSERT INTO uri (id, original_uri, sha256) VALUES (?, ?, ?)"
        cursor = self.get_cursor()
        cursor.execute(cmd, (entry.id, entry.uri, entry.sha256,))
        self.connection.commit()
        cursor.close()

    def update_access_date(self, id):
        Entry.is_valid_id(id)
        cmd = "UPDATE uri SET last_accessed=CURRENT_TIMESTAMP WHERE id=?"
        cursor = self.get_cursor()
        cursor.execute(cmd, (id,))
        self.connection.commit()
        cursor.close()

    def get_entry_from_digest(self, digest):
        digest = Entry.is_valid_digest(digest)
        cmd = "SELECT * FROM uri WHERE sha256=?"
        cursor = self.get_cursor()
        cursor.execute(cmd, (digest,))
        query = cursor.fetchall()
        cursor.close()
        result = []
        for id, uri, digest, created_time, last_accessed_time in query:
            entry = Entry(id, uri, created_time, last_accessed_time)
            entry.set_digest(digest)
            result.append(entry)
            
        return result

    def get_entry_from_id(self, id):
        Entry.is_valid_id(id)
        cmd = "SELECT * FROM uri WHERE id=?"
        cursor = self.get_cursor()
        cursor.execute(cmd, (id,))
        query = cursor.fetchall()
        cursor.close()
        result = []
        for id, uri, digest, created_time, last_accessed_time in query:
            entry = Entry(id, uri, created_time, last_accessed_time)
            entry.set_digest(digest)
            result.append(entry)
        
        return result

    def ping(self):
        return self.connection.ping()

    def close_connection(self):
        self.connection.close()
        self.connection = None
    
if "__main__" == __name__:
    from config_parser import ConfigParser
    ConfigParser()
    user = ConfigParser.get_config()["database"]["user"]
    password = ConfigParser.get_config()["database"]["password"]
    db = DBClient(user, password)