# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import toml

class ConfigParser:

    _instance = None

    def __new__(cls, path="/etc/uri_shortener/config.toml"):
        if not isinstance(path, str):
            raise TypeError("Configuration file path not a string")
        
        if cls._instance is None:
            cls._instance = super(ConfigParser, cls).__new__(cls)
            cls.path = path
            cls.config = {}
        cls.parse_config()
        return cls._instance

    @staticmethod
    def get_path():
        '''
        Return
        str: Configuration file path
        '''
        return ConfigParser.path
    
    @staticmethod
    def get_config():
        """
        Return
        dict: Empty dictionary / dictionary with parsed configuration
        """
        return ConfigParser.config

    @staticmethod
    def parse_config():
        """
        Return
        dict: Parsed configuration
        """
        if ConfigParser._instance == None:
            raise ValueError("ConfigParser singleton not initialized.")
        
        with open(ConfigParser.path, "r") as f:
            ConfigParser.config = toml.load(f)
        
        return ConfigParser.config