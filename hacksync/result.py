from typing import Any, Iterator
from threading import Condition, Lock

class Result:
    def __init__(self) -> None:
        self.__result: Any = None
        self.__done: bool = False
        self.__lock = Lock()
        self.__condition = Condition(self.__lock)

    def __await__(self) -> Iterator[Any]:
        '''
        This would be cool to use the "await result" syntax, but you can't have 
            await keywords outside of an async function, which is what we are avoiding.
        '''
        with self.__condition:
            self.__condition.wait_for(self.__done)
            yield self.__result

    def get(self) -> Any:
        with self.__condition:
            self.__condition.wait_for(lambda : self.__done)
            return self.__result

    def resolve(self, result: Any) -> None:
        with self.__lock:
            self.__done = True
            self.__result = result
            self.__condition.notify()
