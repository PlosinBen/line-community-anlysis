from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self._data = {}
        load_dotenv()

    def _getter(self, key: str, default: str = None):
        if key not in self._data:
            self._data[key] = getenv(key)
        return self._data.get(key)

    @property
    def data_path(self, default: str = './data'):
        return self._getter('DATA_PATH', default)

    @property
    def resource_data_path(self, default: str = None):
        return '{}/resource'.format(self.data_path)

    @property
    def process_data_path(self, default: str = None):
        return '{}/process'.format(self.data_path)

    @property
    def message_data_path(self, default: str = None):
        return '{}/message'.format(self.data_path)


config = Config()
