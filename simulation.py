import network
import file_out
import pprint
from time import perf_counter

log = file_out.SimulationLog()

class Simulation:

    def __init__(self, params : {}, cycle : int, mode : str) -> None:
        self.mode = params.get('mode') 
        self.sx = params.get('sx')
        self.sy = params.get('sy')
        self.su = params.get('su')
        self.cycles = params.get('cycles')
        self._network = network.Network()

    def run(self) -> float:
        time_str = perf_counter()
        self._network.add_agents(self.sx, 'x')
        self._network.add_agents(self.sy, 'y')
        self._network.add_agents(self.su, 'u')
        if (self.mode == "fixation"):
            run_to_fixation(self._network)
        else:
            run_to_cycle(self._network, self.cycles)
        time_end = perf_counter()
        self._network.clear_agents()
        return time_str - time_end

class Master_Simulation():

    def __init__(self, params : {}) -> None:
        self.trials = params.get('trials')
        self.params = params.copy()
        self.mode = params.get('mode').upper()
        if self.mode == 'CYCLES':
            self.params["cycles"] = int(input('How many cycles will this run for?'))
        elif self.mode != 'FIXATION':
            raise Exception('This simulation type is unrecognised.')

    def __str__(self) -> None:
        """Prints the parameters of the simulations."""
        return pprint.pformat(self.params)
    
    def run(self) -> None:
        """Runs a single trial of the simulation for established trials."""
        for i in range(1, self.trials + 1):
            sim_cycle = Simulation(self.params, i, self.mode)
            print('Running Trial #%3d' % i)
            elapsed = sim_cycle.run()
            print("Done. Time Elapsed: %3f" % elapsed)
            del sim_cycle
        print("All trials complete.")
        log.save_file()

def run_to_cycle(net : network.Network,  cycles : int) -> None:
    """Runs the simulation for a set number of cycles."""
    log.add_row(0, net.count_beliefs()) #Print starting row
    for i in range(1, cycles + 1):
        net.aprox_maj()
        log.add_row(i, net.count_beliefs())
    log.inc_trial()

def run_to_fixation(net : network.Network) -> None:
    """Runs the simulation until there are no more undecided agents."""
    log.add_row(0, net.count_beliefs()) #Print starting row
    i = 0
    while net.count_beliefs().get('nu') != 0:
        i += 1
        net.aprox_maj()
        log.add_row(i, net.count_beliefs())
    log.inc_trial()