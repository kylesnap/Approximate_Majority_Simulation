#!/usr/bin/env bash

###ARG PARSING FUNCTIONS###
argparse() {
  argparser=$(mktemp 2>/dev/null || mktemp -t argparser)
  cat >"$argparser" <<EOF
from __future__ import print_function
import sys
import argparse
import os
class MyArgumentParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        """Print help and exit with error"""
        super(MyArgumentParser, self).print_help(file=file)
        sys.exit(1)
parser = MyArgumentParser(prog=os.path.basename("$0"),
            description="""$ARGPARSE_DESCRIPTION""")
EOF

  # stdin to this function should contain the parser definition
  cat >>"$argparser"

  cat >>"$argparser" <<EOF
args = parser.parse_args()
for arg in [a for a in dir(args) if not a.startswith('_')]:
    key = arg.upper()
    value = getattr(args, arg, None)
    if isinstance(value, bool) or value is None:
        print('{0}="{1}";'.format(key, 'yes' if value else ''))
    elif isinstance(value, list):
        print('{0}=({1});'.format(key, ' '.join('"{0}"'.format(s) for s in value)))
    else:
        print('{0}="{1}";'.format(key, value))
EOF

  # Define variables corresponding to the options if the args can be
  # parsed without errors; otherwise, print the text of the error
  # message.
  if python "$argparser" "$@" &>/dev/null; then
    eval "$(python "$argparser" "$@")"
    retval=0
  else
    python "$argparser" "$@"
    retval=1
  fi

  rm "$argparser"
  return $retval
}

###END OF ARG PARSER###

#Prepare arguments for parsing
ARGPARSE_DESCRIPTION="Repeats the simulation with a given algorithm and from s-agent count [x, y] in steps of 'n'."
argparse "$@" <<EOF || exit 1
parser.add_argument('-s', '--seed', action='store_true',
                    default=False, help='seeds the simulation')
parser.add_argument("model", help="interaction model used", choices=['am', 'bam', 'ac'])
parser.add_argument('x', help='starting number of s-agents')
parser.add_argument('y', help='final number of s-agents')
parser.add_argument('n', help='increment step for s-agents between simulations')
parser.add_argument('p', help='probability that s-agents learn')
EOF

#When run, print message before running python code.
printf "\nThe simulation will be performed with '%s' and from s-agent count [%d, %d] in steps of %d.
The simulation will run for 10,000 cycles, 20 trials, and with 500 x-agents to start.\n\n" "$MODEL" "$X" "$Y" "$N"

read -r -p "Proceed? [Y/N] " response
if ! [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
  echo Aborted!
  exit 1
fi

#If yes, run simulations. Seed if necessary.
log_title=$(printf "./output/%s_logfile_%s.txt" "$MODEL" "$(date +'%d%m%Y')")
mkdir "./output" && touch "$log_title"
if [[ $SEED ]]; then
  for ((i = X; i <= Y; i += N)); do
    echo Running with s = $i. SEED ON.
    ./main.py -s "$MODEL" 20 10000 500 0 0 $i "$P" >>"$log_title"
  done
else
  for ((i = X; i <= Y; i += N)); do
    echo Running with s = $i. SEED OFF.
    ./main.py "$MODEL" 20 10000 500 0 0 $i "$P" >>"$log_title"
  done
fi

echo Done!
exit 0
