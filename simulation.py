import network
import pprint
from time import perf_counter

class Simulation:

    def __init__(self, params : {}, cycle : int) -> None:
        self.mode = params.get('mode') 
        self.sx = params.get('sx')
        self.y = params.get('sy')
        self.su = params.get('su')
        self._network = network.Network()

    def run(self) -> float:
        time_str = perf_counter()
        time_end = perf_counter()
        return time_str - time_end

class Master_Simulation():

    def __init__(self, params : {}) -> None:
        self.cycles = params.get('cycles')
        self.params = params.copy()

    def __str__(self) -> None:
        """Prints the parameters of the simulations."""
        return pprint.pformat(self.params)
    
    def run(self) -> None:
        """Runs a single cycle of the simulation for established cycles."""
        for i in range(1, self.cycles + 1):
            sim_cycle = Simulation(self.params, i)
            print('Running Cycle #%3d' % i)
            elapsed = sim_cycle.run()
            print("Done. Time Elapsed: %3f" % elapsed)
            del sim_cycle
        print("All cycles complete.")