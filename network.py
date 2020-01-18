import agents
import random
import warnings
from typing import Dict, Type

ACCEPTED_STATES = ['x', 'y', 'u']

class Network:

    def __init__(self) -> None:
        """Constructs empty dictionary representing network."""
        self.__units : Dict() = dict()
        self.length : int = 0

    def add_agents(self, n : int, state : str) -> None:
        """Adds 'n' number of 'state' agents."""
        if state not in ACCEPTED_STATES:
            warnings.warn("Agents of this state are not supported. No agents were added.")
            return
        for i in range(self.length, self.length + n):
            self.length += 1
            self.__units[self.length] = agents.Agent(self.length, state)
        del i
        print("%d number of %s-agents added to network." % (n, state))

    def count_beliefs(self) -> dict():
        """Returns a dictionary of agent type counts."""
        x = y = u = 0
        for agent in self.__units.values():
            state = agent.state
            if state == 'x':
                x += 1
            elif state == 'y':
                y += 1
            elif state == 'u':
                u += 1
            else:
                raise ValueError('Unsupported agent found in network.')
        return {'nx' : x, 'ny' : y, 'nu' : u}

    def clear_agents(self) -> None:
        """Clears network."""
        self.__units.clear()
        self.length = 0
        print("All units removed from the network.")

    def print_all(self) -> None:
        """Prints a list of all the IDs and Agents."""
        print("There are %d agents in this network.\n" % self.length)
        for agent in self.__units.values():
            print(agent)

    def aprox_maj(self, id_init : int, id_recip : int) -> agents.Agent:
        """The approximate majority algorithm for an exchange between two agents."""
        init : agents.Agent = self.__units.get(id_init)
        recip : agents.Agent = self.__units.get(id_recip)

        if init is None or recip is None:
            warnings.warn('ID[s] provided were not found in network.')
            return None

        if (init is recip or
        init.get_state() is recip.get_state() or
        init.get_state() is 'u'):
            pass
        elif (recip.get_state() is 'u'):
            recip.set_state(init.get_state())
        else:
            recip.set_state('u')

        return recip