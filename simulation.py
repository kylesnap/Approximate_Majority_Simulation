import pprint
from time import perf_counter

import file_out
import network

log = file_out.SimulationLog()


class Simulation:

    def __init__(self, params: {}, cycle: int) -> None:
        self.sx = params.get('sx')
        self.sy = params.get('sy')
        self.sxy = params.get('sxy')
        self.ss = params.get('ss')
        self.model = params.get('model')
        self.cycles = params.get('cycles')
        self._network = network.Network()

    def run(self) -> float:
        """Prepares a network, then runs cycles number of interactions between agents."""
        time_str = perf_counter()
        self._network.add_agents(self.sx, 'x')
        self._network.add_agents(self.sy, 'y')
        self._network.add_agents(self.sxy, 'xy')
        self._network.add_agents(self.ss, 's')
        run_to_cycle(self._network, self.model, self.cycles)
        time_end = perf_counter()
        self._network.clear_agents()
        return time_end - time_str


class Master_Simulation():

    def __init__(self, params: {}) -> None:
        self.trials = params.get('trials')
        self.params = params.copy()

    def __str__(self) -> None:
        """Prints the parameters of the simulations."""
        return pprint.pformat(self.params)

    def run(self) -> None:
        """Runs a single trial of the simulation for established trials."""
        for i in range(1, self.trials + 1):
            sim_cycle = Simulation(self.params, i)
            print('Running Trial #%3d' % i)
            elapsed = sim_cycle.run()
            print("Done. Time Elapsed: %3f" % elapsed)
            del sim_cycle
        print("All trials complete.")
        log.save_file()


def run_to_cycle(net: network.Network, alg: str, cycles: int) -> None:
    """Runs the simulation for a set number of cycles."""
    log.add_row(0, net.count_beliefs())  # Print starting row
    for i in range(1, cycles + 1):
        if alg == 'AM':
            net.am()
        elif alg == 'BAM':
            net.bam()
        elif alg == 'AC':
            net.ac()
        else:
            raise ValueError('Algorithm not recognised.')
        log.add_row(i, net.count_beliefs())
    log.inc_trial()
