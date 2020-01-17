import agents

class Network:

    def __init__(self):
        """Constructs empty dictionary representing network."""
        self.__units = dict()
        self.length = 0

    def add_agents(self, n: int, state: str):
        """Adds 'n' number of 'state' agents."""
        for i in range(self.length, self.length + n):
            self.length += 1
            self.__units[self.length] = agents.Agent(self.length, state)
        print("%d number of %s-agents added to network." % (n, state))

    def count_beliefs(self):
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

    def clear_agents(self):
        """Clears network."""
        self.__units.clear()
        self.length = 0
        print("All units removed from the network.")

    def print_all(self):
        """Prints a list of all the IDs and Agents."""
        print("There are %d agents in this network." % self.length)
        for agent in self.__units.values():
            print(agent)