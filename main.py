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
    mode = input("Please enter the simulation mode. [Either 'Fixation' or 'Cycles']")
    sx = int(input("Please enter the starting number of  'x' agents:"))
    sy = int(input("Please enter the starting number of  'y' agents:"))
    su = int(input("Please enter the number of  'u' agents:"))
    trials = int(input("Please enter the number of  trials:"))
    mean = float(input("Please enter the mean 'p' value [0, 1]:"))
    sd = float(input("Please enter the std of the 'p' value:"))
    params = {'mode' : mode, 'sx' : sx, 'sy' : sy, 'su' : su, 'trials' : trials, 'mean' : mean, 'sd' : sd}
    return params

if __name__ == "__main__":
    main()