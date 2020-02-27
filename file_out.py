from datetime import datetime
import subprocess
import pandas as pd
import numpy as np


class SimulationLog:

    def __init__(self) -> None:
        self._file = pd.DataFrame()
        self._trial = 1

    def inc_trial(self) -> None:
        """Increases the 'trial' row by one."""
        self._trial = self._trial + 1

    def add_row(self, cycle: int, counts: {}) -> None:
        """Adds a row to the dataframe."""
        self._file = self._file.append(
            pd.Series(data=(cycle, counts.get('nx'), counts.get('ny'),
                      counts.get('nxy'), counts.get('ns')),
            ),
            ignore_index=True,
        )

    def get_file(self) -> pd.DataFrame:
        return self._file

    def save_file(self) -> None:
        """Save log file with current date and time."""
        today = datetime.now()
        file_name = str("./Data/SIMULATION_%s.csv" % today.strftime("%d_%m_%Y_%H%M"))
        self._file.index.name = 'TRIAL'
        # print(self._file.head(10))
        try:
            output_dir = subprocess.check_call(["mkdir", "p", "Data"])
            f = open(file_name, "w")
            self._file.to_csv(f)
        except subprocess.CalledProcessError:
            f = open("SIMULATION_ % s.csv"% today.strftime("%d_%m_%Y_%H%M"), "w")
            self._file.to_csv(f)

        print('File Printed to %s' % file_name)
