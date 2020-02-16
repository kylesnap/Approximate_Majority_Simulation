import agents
import random
import warnings
from typing import Dict, Type

ACCEPTED_STATES = ['x', 'y', 'xy', 's']


class Network:

    def __init__(self) -> None:
        """Constructs empty dictionary representing network."""
        self.__units = {}
        self.length = 0

    def add_agents(self, n: int, state: str) -> None:
        """Adds 'n' number of 'state' agents."""
        if state not in ACCEPTED_STATES:
            warnings.warn("Agents of this state are not supported. No agents were added.")
            return
        for i in range(self.length, self.length + n):
            self.length += 1
            self.__units[self.length] = agents.Agent(self.length, state)

    def count_beliefs(self) -> dict():
        """Returns a dictionary of agent type counts."""
        x = y = xy = 0
        for agent in self.__units.values():
            state = agent.get_state
            if state == 'x':
                x = x + 1
            elif state == 'y':
                y = y + 1
            else:
                xy = xy + 1
        counts = {'nx': x, 'ny': y, 'nxy': xy}
        return counts

    def clear_agents(self) -> None:
        """Clears network."""
        self.__units.clear()
        self.length = 0
        # For testing
        # print("All units removed from the network.")

    def print_all(self) -> None:
        """Prints a list of all the IDs and Agents."""
        print("There are %d agents in this network.\n" % self.length)
        for agent in self.__units.values():
            print(agent)

    def bam(self, i: int = -1, r: int = -1) -> agents.Agent:
        """Implements the BAM algorithm."""
        if i == -1 or r == -1:
            init = self.__units.get(random.choice(list(self.__units)))
            recip = self.__units.get(random.choice(list(self.__units)))
        else:
            init = self.__units.get(i)
            recip = self.__units.get(r)
        choice = random.choice(['x', 'y'])

        if recip.state == 's':
            pass  # Stubborn agents won't learn.
        elif recip.state == init.state:
            if recip.state == 'xy':   # If both agents are compound, they'll come to both share a state at random.
                recip.state = init.state = choice
        elif init.state == 's':
            if recip.state == 'xy':
                recip.state = 'y'
            elif recip.state == 'x':
                recip.state = 'xy'
        elif init.state == 'xy':  # If the initiator is compound, it will choose to share a state at random.
            if recip.state == choice:
                init.state = choice
            else:
                recip.state = 'xy'
        else:
            if recip.state == 'xy':
                recip.state = init.state
            else:
                recip.state = 'xy'

        return recip


def aprox_maj(self) -> agents.Agent:
    """The approximate majority algorithm for an exchange between two agents."""
    pass
