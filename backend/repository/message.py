from ..core.lib.message import Messages, Message
from ..core.lib.config import config
import pickle
from hashlib import md5


class MessageRepository:
    @staticmethod
    def get(hex_str: str) -> Messages | None:
        mapping = MessageRepository._get_name_by_hash(hex_str)

        if mapping is None:
            return None

        return MessageRepository.get_by_file_name(mapping)

    @staticmethod
    def get_by_file_name(name: str) -> Messages | None:
        file_path = config.get_message_path() / name

        if not file_path.is_file():
            return None

        return pickle.loads(
            file_path.read_bytes()
        )

    @staticmethod
    def get_by_name_version(name: str, version: str) -> Messages | None:
        return MessageRepository.get_by_file_name('{}-{}'.format(name, version))

    @staticmethod
    def _get_name_by_hash(hex_str: str) -> str | None:
        map_file_path = config.get_message_hash_mapping_path() / hex_str

        if map_file_path.is_file():
            return pickle.loads(
                map_file_path.read_bytes()
            )
        else:
            return None

    @staticmethod
    def _save_hash_map(hex_str: str, name: str):
        map_file_path = config.get_message_hash_mapping_path() / hex_str

        map_file_path.write_bytes(
            pickle.dumps(name)
        )

    @staticmethod
    def save(messages: Messages):
        filename = '{}-{}'.format(
            messages.title,
            messages.version
        )

        file_path = config.get_message_path() / filename

        if file_path.exists():
            pass

        messages.hash = md5(filename.encode('utf-8')).hexdigest()

        file_path.write_bytes(
            pickle.dumps(messages)
        )

        MessageRepository._save_hash_map(messages.hash, filename)
