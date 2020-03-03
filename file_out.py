import subprocess
from datetime import datetime

import pandas as pd


class SimulationLog:

    def __init__(self) -> None:
        self._data = {}
        self._trial = 1
        self._nrow = 0

    def inc_trial(self) -> None:
        """Increases the 'trial' col by one."""
        self._trial += 1

    def add_row(self, cycle: int, counts: {}) -> None:
        """Adds a row to the dataframe."""
        self._data[self._nrow] = {'TRIAL': self._trial, 'CYCLE': cycle, 'NX': counts.get('x'), 'NY': counts.get('y'),
                                  'NXY': counts.get('xy'), 'NS': counts.get('s')}
        self._nrow += 1

    def get_file(self) -> {}:
        return self._data

    def save_file(self) -> None:
        """Save log file with current date and time."""
        today = datetime.now()
        file_name = str("./Data/SIMULATION_%s.csv" % today.strftime("%d_%m_%Y_%H%M"))
        df = pd.DataFrame.from_dict(self._data, "index")
        # print(self._file.head(10))
        try:
            output_dir = subprocess.check_call(["mkdir", "-p", "Data"])
            f = open(file_name, "w")
            df.to_csv(f, index=False)
        except subprocess.CalledProcessError:
            f = open("SIMULATION_ % s.csv" % today.strftime("%d_%m_%Y_%H%M"), "w")
            df.to_csv(f, index=False)

        print('File Printed to %s' % file_name)
