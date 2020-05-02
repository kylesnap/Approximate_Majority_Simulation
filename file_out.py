import os
from datetime import datetime

import pandas as pd


class SimulationLog:

    def __init__(self) -> None:
        self._data = {}
        self._trial = 1
        self._nrow = 0
        self._s_start = None

    def inc_trial(self) -> None:
        """Increases the 'trial' col by one."""
        self._trial += 1

    def add_row(self, cycle: int, counts: {}) -> bool:
        """Adds a row to the dataframe. Also gets starting (i.e. maximum) number of s-agents and adds them to a row.
        If network is at stasis (and no learning is possible), then throws false."""
        if self._s_start is None:
            self._s_start = counts.get('s')
        self._data[self._nrow] = {'TRIAL': self._trial, 'CYCLE': cycle, 'NX': counts.get('x'), 'NY': counts.get('y'),
                                  'NXY': counts.get('xy'), 'NS': counts.get('s'), 'SS': self._s_start,
                                  'BOT_P': counts.get('bot_p')}
        self._nrow += 1

        # If the simulation reaches a plateau, then return false (end early).
        if (((counts.get('x', 0) == 0) or (counts.get('y', 0) == 0 and counts.get('s', 0) == 0)) and
            (counts.get('xy', 0) == 0)):
            return False
        else:
            return True

    def get_file(self) -> {}:
        return self._data

    def save_file(self, alg: str) -> None:
        """Save log file with current date and time."""
        today = datetime.now()
        file_name = str("./output/%s_SIMULATIONS_%s.csv" % (alg, today.strftime("%d%m%Y")))
        df = pd.DataFrame.from_dict(self._data, "index")
        try:
            os.mkdir('./output')
        except FileExistsError:
            pass
        try:
            if os.path.exists(file_name):
                f = open(file_name, "a")
                df.to_csv(f, index=False, na_rep=0, header=False)
            else:
                f = open(file_name, "w")
                df.to_csv(f, index=False, na_rep=0)
        except IOError:
            print('IO Error: File did not save.')
        finally:
            f.close()

        print('File Printed to %s' % file_name)