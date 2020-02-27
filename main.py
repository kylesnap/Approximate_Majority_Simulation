import simulation
from typing import Dict

def main() -> None:
    """Controls the simulation."""
    params = control()
    sim = simulation.Master_Simulation(params)
    print("The simulation will be run with the following parameters:")
    print(sim)
    print()
    switch = int(input("Would you like to run this simulation now? [1: Yes, 2: No]"))
    if (switch is 1):
        print("Beginning Simulation!")
        print()
        sim.run()
    else:
        print("Simulation has been aborted.")

def control() -> Dict:
    """Asks the user for simulation parameters."""
    alg = input("Enter either 'AM', 'BAM', or 'AC'")
    if alg not in ['AM', 'BAM', 'AC']:
        raise NameError('Algorithm not-supported. Please ensure your entry is case sensitive.')
    sx = int(input("Please enter the starting number of  'x' agents:"))
    sy = int(input("Please enter the starting number of  'y' agents:"))
    sxy = int(input("Please enter the number of  'xy' agents:"))
    ss = int(input("Please enter the number of  's' agents:"))
    trials = int(input("Please enter the number of  trials:"))
    cycles = int(input('How many cycles will this run for?'))
    params = {'alg': alg, 'sx': sx, 'sy': sy, 'sxy': sxy, 'ss': ss, 'trials': trials, 'cycles': cycles}
    return params

if __name__ == "__main__":
    main()