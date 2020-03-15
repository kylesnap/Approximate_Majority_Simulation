#!/usr/bin/env python3

import argparse
import random
import warnings

import simulation


def main() -> None:
    """Controls the simulation."""
    params = control()
    sim = simulation.Master_Simulation(params)
    print("The simulation will be run with the following parameters:")
    print(sim)
    sim.run()


def control() -> {}:
    """Asks the user for simulation parameters."""

    # First parses all arguments.
    parser = argparse.ArgumentParser(description="Runs a simulation of the effect of stubborn agents on a network of "
                                                 "social learners.")
    parser.add_argument("model", help="interaction model used", choices=['am', 'bam', 'ac'])
    parser.add_argument("trials", help="number of trials to perform", type=int)
    parser.add_argument("cycles", help="number of cycles per trial", type=int)
    parser.add_argument("x", help="starting number of 'x' agents", type=int)
    parser.add_argument("y", help="starting number of 'y' agents", type=int)
    parser.add_argument("xy", help="starting number of 'xy' agents", type=int)
    parser.add_argument("s", help="starting number of 's' agents", type=int)
    parser.add_argument("bot_p", help="probability of bots to learn successfully", type=float)
    parser.add_argument("-s", "--seed", help="seeds random",
                        action="store_true")
    args = parser.parse_args()

    # Then stores sim parameters in dict, and sets seed if req.
    if args.seed:
        random.seed(69)
        warnings.warn("Random was seeded. Run without '-s' switch for genuine results.")
    return {'model': args.model.upper(), 'trials': args.trials, 'cycles': args.cycles,
            'sx': args.x, 'sy': args.y, 'sxy': args.xy, 'ss': args.s, 'bot_p': args.bot_p}


if __name__ == "__main__":
    main()
