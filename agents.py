class Agent:

    def __init__(self, ag_id: int, state: str, p: float) -> None:
        self.ID = ag_id
        self._state = state
        self._p = p

    def __str__(self) -> str:
        """Pretty print."""
        return str("ID: %5d, State: %c, p: %f" % (self.ID, self._state, self._p))

    def __eq__(self, other) -> bool:
        """Returns true when the two agents are the same."""
        if self.ID == other.ID: return True
        return False

    def get_state(self) -> str:
        return self._state

    def set_state(self, value: str) -> object:
        self._state = value

    def get_p(self) -> float:
        return self._p
