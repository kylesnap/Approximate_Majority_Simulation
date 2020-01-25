from typing import List, Type

class Agent:

    def __init__(self, id : int, state: str, p : float) -> None:
        self._ID = id
        self._state = state
        self._p = p

    def __str__(self) -> str:
        """Pretty print."""
        return str("ID: %5d, State: %c, p: %f" % (self._ID, self._state, self._p))

    def __eq__(self, other) -> bool:
        """Returns true when the two agents are the same."""
        if (self._ID == other._ID): return True
        return False

    def get_state(self) -> str:
        return self._state

    def set_state(self, value: str) -> None:
        self._state = value

    def get_p(self) -> float:
        return self._p