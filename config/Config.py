import os
import json
from dotenv import load_dotenv
from osbot_utils.utils.Files import folder_not_exists, path_combine, create_folder, folder_create


FILE_GENERATOR_LOCATION   = path_combine(__file__                , '../../generated_files' )

class Config:

    _instance = None

    def __new__(cls):  # singleton pattern
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.file_generator_location=None
        self.load_values()

    def load_values(self):
        load_dotenv(override=True)
        self.set_generator_location(os.getenv("FILE_GENERATOR_LOCATION" , FILE_GENERATOR_LOCATION ))

        return self

    def ensure_last_char_is_not_forward_slash(self, path: str):
        if path.endswith('/') or path.endswith('\\'):
            path = path[:-1]
        return path

    def set_generator_location(self,generator_location):
        self.file_generator_location = self.ensure_last_char_is_not_forward_slash(generator_location)
        folder_create(self.file_generator_location)

