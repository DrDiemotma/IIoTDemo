import json
import os.path
from threading import Lock
import CollectorNode.CentralConfig.constants as constants

CONFIG_FILE: str = "config.json"
PATH_INIT: str = "path:"

class SingletonMeta(type):
    """
    Thread-safe version of a singleton pattern. Use for configuration managers.
    """
    _instances = {}
    _lock: Lock = Lock()
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    """
    Configuration manager class.
    """
    def __init__(self):
        """
        ctor.
        """
        self._d = dict()
        self._restored = False
        self._lock = Lock()


    def set_entry(self, caller: str, key: str, entry: str | float | int | bool | list[str | float | int | bool],
                  persist: bool = True):
        """
        Set an entry. Note if you don't specify the caller or the cey, the data will not be stored.

        :param caller: Identifier for who is calling. Use "__name__" or "__file__" depending on the context.
        :param key: Key of the parameter to store or update.
        :param entry: Entry to store.
        :param persist: whether to automatically persist. This might be slow, so you might want to persist manually.
        :return: None.
        """
        if caller is None or key is None:
            return

        if not isinstance(caller, str):
            caller = str(caller)

        self.restore()

        if caller not in self._d:
            self._d[caller] = dict()

        if caller.startswith("/"):
            caller = PATH_INIT + caller

        self._d[caller][key] = entry
        if persist:
            self.persist()

    def get_entry(self, caller: str, key: str,
                  default: str | float | int | bool | list[str | float | int | bool] | None = None) \
            -> str | float | int | bool | list[str | float | int | bool] | None:
        """
        Get an entry from the configuration.
        :param caller: Identifier for who is calling. Use "__name__" or "__file__" depending on the context.
        :param key: Key of the parameter to access.
        :param default: A default value. Will be added if not present in the dictionary.
        :return: A value stored in the configuration. If not stored, None is returned.
        """
        if caller is None or key is None:
            return default

        self.restore()

        if not self._restored:
            return default

        if not isinstance(caller, str):
            caller = str(caller)

        if caller.startswith("/"):
            caller = PATH_INIT + caller

        if not caller in self._d:
            return default

        d = self._d[caller]
        if key not in d:
            d[key] = default
            return default

        return d[key]

    def delete_entry(self, caller: str, key: str) -> None:
        """
        Delete a given parameter.
        :param caller: Identifier for who is calling. Use "__name__" or "__file__" depending on the context.
        :param key: Key of the parameter to delete.
        :return: None.
        """
        if caller is None or key is None:
            return None

        if not isinstance(caller, str):
            caller = str(caller)

        if caller.startswith("/"):
            caller = PATH_INIT + caller

        if caller not in self._d:
            return None

        d: dict = self._d[caller]
        if key in d:
            d.pop(key)

    def persist(self):
        """
        Save the data to the hard drive.
        :return:
        """
        with self._lock, open(CONFIG_FILE, "w") as f:
            json.dump(self._d, f, indent=4)

    def restore(self):
        if self._restored:
            return

        if os.path.isfile(CONFIG_FILE):
            with self._lock, open(CONFIG_FILE, "r") as f:
                self._d = json.load(f)

            for namespace, entries in constants.DEFAULT_TUPLES.items():
                if not namespace in self._d:
                    current_dict = dict()
                    self._d[namespace] = current_dict
                    for key, value in entries.items():
                        current_dict[key] = value

            self._restored = True
