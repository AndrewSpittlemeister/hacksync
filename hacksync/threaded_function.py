from typing import Callable, Any, Tuple, Dict
from threading import Thread, Event, Lock
from queue import SimpleQueue as Queue
from uuid import uuid4, UUID

from .result import Result


class ThreadedFunction(Thread):
    def __init__(self, function: Callable) -> None:
        super().__init__(daemon=True)

        self.__stop_event = Event()
        self.__function = function
        self.__call_queue = Queue()
        self.__result_map: Dict[UUID, Result] = dict()

    def run(self) -> None:
        while not self.__stop_event.is_set():
            uuid, args, kwargs = self.__call_queue.get()
            if (args != ()):
                if (kwargs != {}):
                    self.__result_map[uuid].resolve(self.__function(*args, **kwargs))
                else:
                    self.__result_map[uuid].resolve(self.__function(*args))
            else:
                if (kwargs != {}):
                    self.__result_map[uuid].resolve(self.__function(**kwargs))
                else:
                    self.__result_map[uuid].resolve(self.__function())

    def stop(self) -> None:
        self.__stop_event.set()
        Thread.join(self)

    def __call__(self, *args, **kwargs) -> Any:
        uuid = uuid4()
        result = Result()
        self.__call_queue.put_nowait((uuid, args, kwargs))
        self.__result_map[uuid] = result
        return result

    def __del__(self) -> None:
        self.stop()