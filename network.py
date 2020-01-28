import random
import warnings

from scipy.stats import truncnorm

import agents

ACCEPTED_STATES = ['x', 'y', 'u']
warnings.simplefilter('once', UserWarning)

class Network:

    def __init__(self) -> None:
        """Constructs empty dictionary representing network."""
        self.size = 0
        self.rep_cycles = 0
        self.counts = {}
        self.__units = {}

    def add_agents(self, n: int, state: str, gen) -> None:
        """Adds 'n' number of 'state' agents with a random p given the generator."""
        if state not in ACCEPTED_STATES:
            warnings.warn("Agents of this state are not supported. No agents were added.")
            return
        for i in range(self.size, self.size + n):
            self.size += 1
            self.__units[self.size] = agents.Agent(self.size, state, gen.make_p())
        # For testing
        # print("%d number of %s-agents added to network." % (n, state))

    def count_beliefs(self) -> dict():
        """Returns a dictionary of agent type counts."""
        x = y = u = 0
        for agent in self.__units.values():
            state = agent.get_state()
            if state == 'x':
                x = x + 1
            elif state == 'y':
                y = y + 1
            else:
                u = u + 1
        return {'nx': x, 'ny': y, 'nu': u}

    def clear_agents(self) -> None:
        """Clears network."""
        self.__units.clear()
        self.size = 0
        # For testing
        # print("All units removed from the network.")

    def print_all(self) -> None:
        """Prints a list of all the IDs and Agents."""
        print("There are %d agents in this network.\n" % self.size)
        for agent in self.__units.values():
            print(agent)

    def aprox_maj(self) -> agents.Agent:
        """The approximate majority algorithm for an exchange between two agents."""
        init = self.__units.get(random.choice(list(self.__units)))
        recip = self.__units.get(random.choice(list(self.__units)))

        if init is None or recip is None:
            warnings.warn('ID[s] provided were not found in network.')
            return None

        self.rep_cycles += 1

        # Check strength of prior to see whether learning will be successful
        if recip.get_p() <= random.random():
            return None

        if (init == recip or
                init.get_state() == recip.get_state() or
                init.get_state() == 'u'):
            pass
        elif (recip.get_state() == 'u'):
            recip.set_state(init.get_state())
            self.rep_cycles = 0
        else:
            recip.set_state('u')
            self.rep_cycles = 0

        return recip

    def is_fixation(self) -> bool:
        """Checks whether simulation has reached fixation."""
        is_fixed = False
        new_counts = self.count_beliefs()
        # Def #1 of fixation: Only one kind of decided unit in network
        if (new_counts.get('nu') == 0) & ((new_counts.get('nx') != 0) ^ (new_counts.get('ny') != 0)):
            is_fixed = True

        # Def #2: 100 cycles have passed without any changes.
        if self.rep_cycles > 100:
            is_fixed = True

        return is_fixed


class P_Generator:

    def __init__(self, mean: float, sd: float) -> None:
        low = 0
        upp = 1
        self._mean = mean
        try:
            self._gen = truncnorm(
                (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
        except ZeroDivisionError:
            warnings.warn("SD is 0; setting all agent's 's' to the mean.")
            self._gen = None

    def make_p(self):
        """Creates a new rand float based on the distribution generated."""
        if self._gen is None:
            return self._mean
        else:
            return self._gen.rvs()
