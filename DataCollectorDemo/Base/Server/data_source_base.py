
import abc
from Base.Server.server_base import ServerBase
from typing import Callable, Any

class DataSourceBase(ServerBase, abc.ABC):

    _callback: Callable[[Any], None]
    @property
    def new_data_callback(self):
        return self._callback

    @abc.abstractmethod
    @new_data_callback.setter
    def new_data_callback(self, callback: Callable[[Any], None]):
        self._callback = callback
