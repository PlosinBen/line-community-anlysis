from os import getenv
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


class Config:
    def __init__(self):
        self._data = {}
        load_dotenv()

        data_path = Path(self.data_path)
        if not data_path.is_dir():
            data_path.mkdir()

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

    def _create_path(self, path: str, *args) -> Path:
        target = Path(path, *args)

        if not target.exists():
            target.mkdir()

        return target

    def get_analysis_path(self) -> Path:
        return self._create_path(self.data_path, 'mapping')

    def get_message_path(self) -> Path:
        return self._create_path(self.message_data_path)

    def get_message_hash_mapping_path(self):
        return self._create_path(self.message_data_path, 'mapping')


config = Config()
