class Agent:

    def __init__(self, id: int, state: str) -> None:
        self._ID = id
        self._state = state

    def __str__(self) -> str:
        """Pretty print."""
        return str("ID: %5d, State: %c" % (self._ID, self._state))

    def __eq__(self, other) -> bool:
        """Returns true when the two agents are the same."""
        if (self._ID == other._ID):
            return True
        return False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_val: str):
        self._state = new_val
