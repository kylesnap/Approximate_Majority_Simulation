from typing import List
from scipy.stats import truncnorm

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

class P_Generator:

    def __init__(self) -> None:
        mean = float(input("What is the mean of your p distribution? [0.0, 1.0]"))
        sd = float(input("What is the standard deviation of your p distribution?"))
        low = 0
        upp = 1
        self._gen = truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

    def get_p(self):
        return self._gen.rvs()