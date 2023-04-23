import pickle
import abc
from pathlib import Path
from urllib import request
from .config import config
from hashlib import md5


def download_resource(url: str, filename: str = None) -> str:
    filename = md5(url.encode('utf-8')).hexdigest() if filename is None else filename

    filepath = Path(config.resource_data_path, filename).with_suffix(Path(url).suffix)

    if not filepath.is_file():
        request.urlretrieve(url, filepath)

    return str(filepath)


def process_cache(name: str, version: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            filepath = Path(config.process_data_path, name)
            if not filepath.is_dir():
                filepath.mkdir()

            filepath = filepath / version

            if filepath.exists():
                print("{} {} already exists, use cache".format(name, version))

                return pickle.loads(
                    filepath.read_bytes()
                )

            result = func(*args, **kwargs)

            filepath.write_bytes(
                pickle.dumps(result)
            )

            return result

        return wrapper

    return decorator


class Action(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def usage():
        return NotImplemented

    @staticmethod
    @abc.abstractmethod
    def execute(args: list[str]):
        return NotImplemented
