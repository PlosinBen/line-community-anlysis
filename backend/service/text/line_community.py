import logging
from pathlib import Path
from backend.core.conversation_message import parse_to_message, get_name_version
from backend.core.error_exception import FileProcessing, FileNotExistsException
from backend.core.lib import Messages, config
from backend.service.text.report import get_basic_statistics
import pickle
from backend.repository.message import MessageRepository


def analysis(hash_name: str) -> dict:
    analysis_path = config.get_analysis_path() / hash_name

    if analysis_path.exists():
        analysis_data = pickle.loads(
            analysis_path.read_bytes()
        )

        if analysis_data is FileProcessing:
            raise FileProcessing

    else:
        analysis_path.write_bytes(
            pickle.dumps(FileProcessing())
        )

        analysis_data = get_basic_statistics(
            get_message_data(hash_name)
        ).get_result()

        analysis_path.write_bytes(
            pickle.dumps(analysis_data)
        )

    return analysis_data


def save_message_data(filepath: Path) -> str:
    if not filepath.is_file():
        raise FileNotExistsException

    name, version = get_name_version(filepath)
    logging.info('%s, %s', name, version)

    messages = MessageRepository.get_by_name_version(name, version)

    if messages is None:
        messages = parse_to_message(filepath)

        MessageRepository.save(messages)

    return messages.hash


def get_message_data(hash_name) -> Messages:
    messages = MessageRepository.get(hash_name)

    if messages is None:
        raise FileNotExistsException

    return messages
