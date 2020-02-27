import random
import warnings
import agents

from collections import Counter

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
        counts = Counter()
        for agent in self.__units.values():
            counts[f"n{agent.state}"]+=1
        return dict(counts)

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

    ########DO NOT TOUCH ANYTHING BELOW THIS LINE PLEASE##########
    ##############################################################

    def choose_two(self, i: int, r: int):
        """Takes two IDs in the network, and returns their respective units. Chooses at random if unspecified."""
        if i == 0:
            init = self.__units.get(random.choice(list(self.__units)))
        else:
            init = self.__units.get(i)
        if r == 0:
            recip = self.__units.get(random.choice(list(self.__units)))
        else:
            recip = self.__units.get(r)
        return init, recip

    def bam(self, i: int = 0, r: int = 0) -> agents.Agent:
        """Implements the binary agreement model algorithm."""
        init, recip = self.choose_two(i, r)
        choice = random.choice(['x', 'y'])

        if recip.state == 's':
            pass  # Stubborn agents won't learn.
        elif recip.state == init.state:
            if recip.state == 'xy':  # If both agents are compound, they'll come to both share a state at random.
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

    def am(self, i: int = 0, r: int = 0) -> agents.Agent:
        """Implements the approximate majority algorithm."""
        init, recip = self.choose_two(i, r)

        if recip.state == 's' or recip.state == init.state or init.state == 'xy':
            pass
        elif init.state == 's':  # S agents will espouse the y belief
            if recip.state == 'xy':
                recip.state = 'y'
            elif recip.state == 'x':
                recip.state = 'xy'
        else:  # Agents who receive a belief they do not share will be swapped either to xy or to the initiators state.
            if recip.state == 'xy':
                recip.state = init.state
            else:
                recip.state = 'xy'

        return recip

    def ac(self, i: int = 0, r: int = 0) -> agents.Agent:
        """Implements the always-copy algorithm."""
        init, recip = self.choose_two(i, r)

        if recip.state == 's' or recip.state == init.state:
            pass
        elif init.state == 's':  # S agents will espouse the y belief
            recip.state = 'y'
        else:
            recip.state = init.state

        return reci
