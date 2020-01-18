from typing import List

class Agent:

    def __init__(self, id, state) -> None:
        self._ID : int = id
        self._state : str = state

    def __str__(self) -> str:
        """Pretty print."""
        return str("ID: %5d, State: %c" % (self._ID, self._state))

    def __eq__(self, other) -> bool:
        """Returns true when the two agents are the same."""
        if (self._ID == other._ID): return True
        return False

    def get_state(self) -> str:
        return self._state

    def set_state(self, value: str) -> None:
        self._state = value