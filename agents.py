from typing import List


class Agent:

    def __init__(self, id: int, state: str) -> None:
        self._ID = id
        self.__state = state

    def __str__(self) -> str:
        """Pretty print."""
        return str("ID: %5d, State: %2s" % (self._ID, self.__state))

    def __eq__(self, other) -> bool:
        """Returns true when the two agents are the same."""
        if (self._ID == other._ID): return True
        return False

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, state: str) -> None:
        self.__state = state
