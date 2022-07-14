"""
     This file is part of ReproUI.

    ReproUI is free software: you can redistribute it and/or modify it under
    the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    ReproUI is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
    details.

    You should have received a copy of the GNU General Public License along
    with ReproUI. If not, see <https://www.gnu.org/licenses/>.
"""
__author__ = "Echedey Luis Álvaerz"
__copyright__ = "Copyright 2022, Echedey Luis Álvarez"
__credits__ = ["Echedey Luis Álvarez"]
__license__ = "GPL v3"
__version__ = "1.0.0"
__status__ = "Prototype"
__doc__ = """ReproUI is a GUI application designed to aid in the 3D printing
service of CREA, UPM. It accesses a Google Spreadsheet and shows a list of
pending orders"""

import os
import sys
from typing import Optional

import tomli
import pandas as pd
# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QIcon
# pylint: enable=no-name-in-module

from google_flow import GoogleSpreadSheetInterface
from panel_ui import PanelUI
import constants

SECRETS_PATH = '.\\secrets'
CONFIG_FILE = os.path.join(SECRETS_PATH, 'config.toml')
DATA_RANGE = 'HojaA!A2:W'  # First row is col names


class ReproUIApp(QMainWindow):
    """Main class app of ReproUI"""
    def __init__(self, parent: Optional['QWidget']) -> None:
        super().__init__(parent=parent)

        self.setWindowTitle('ReproUI')
        self.setWindowIcon(QIcon(os.path.join('.\\assets', 'logo_256.png')))

        # Initialize configuration
        if(os.path.exists(CONFIG_FILE) and os.path.isfile(CONFIG_FILE)):
            with open(CONFIG_FILE, 'rb') as cf_file:
                self.config = tomli.load(cf_file)
        else:
            raise IOError('Configuration file not found')

        self._init_timers()
        self._init_ss_interface()

        self.panel_ui = PanelUI(
            self,
            self._order_interaction
        )
        self.setCentralWidget(self.panel_ui)

        self._fetch_orders_and_update_panel()

        # Open the qss styles file and read in the css-alike styling code
        with open('assets\\styles\\styles.qss', 'r', encoding='utf-8') as style_fl:
            style = style_fl.read()
            self.setStyleSheet(style)

    def _init_timers(self) -> None:
        self._update_delay_timer = QTimer(self)
        self._update_delay_timer.setSingleShot(True)
        self._update_delay_timer.setTimerType(Qt.TimerType.CoarseTimer)
        self._update_delay_timer.setInterval(
            int(self.config['DB_UPDATE_DELAY']*1000)
        )
        self._update_delay_timer.timeout.connect(self._updater_slot)

        self._retrieve_interval_timer = QTimer()
        self._retrieve_interval_timer.setSingleShot(False)
        self._retrieve_interval_timer.setTimerType(Qt.TimerType.VeryCoarseTimer)
        self._retrieve_interval_timer.setInterval(
            int(self.config['DB_RETRIEVE_INTERVAL']*1000)
        )
        self._retrieve_interval_timer.timeout.connect(self._retriever_slot)

    # Google SpreadSheet functions
    def _init_ss_interface(self) -> None:
        self._ssheet_inter = GoogleSpreadSheetInterface(
            secrets_path=SECRETS_PATH,
            spreadsheet_id=self.config['SPREADSHEET_ID']
        )

    def _read_ss(self) -> pd.DataFrame:
        try:
            orders_raw = self._ssheet_inter.read_range(DATA_RANGE)
            orders_df = pd.DataFrame(
                columns=constants.COLUMN_NAMES,
                # Make sure input is all same length as column names [23]
                data=[order+[''] if len(order) == 22 else order
                      for order in orders_raw]
                )
            orders_df = (orders_df
                        # .astype(constants.COLUMN_DTYPES)  # Useless
                        .dropna(thresh=18)
                        )

            # Yeah, we shouldn't show all the name. Privacy protection first.
            def privacy_protect_name(name):
                name_splitted = name.split()
                return ' '.join([name_splitted[0]] + [nm[:1].upper()+'.'
                                for nm in name_splitted[1:]])
            orders_df['NAME'] = orders_df['NAME'].map(privacy_protect_name)
            return orders_df

        except TypeError as err:
            print('Error reading orders. Check database integrity.')
            print(err)
            return None

    def _update_ss(self, orders_df: pd.DataFrame):
        # Here we only update what might have changed
        # Prevents conflicts
        self._ssheet_inter.update_range(
            range_=constants.cols2_a1_notation('APPROVED','PAID'),
            values=orders_df.loc[:,'APPROVED':'PAID'].values.astype(str).tolist()
        )

    @pyqtSlot()
    def _updater_slot(self):
        """
        Wrapper to call ._update_ss(orders) with the dataframe argument
        """
        print('Timer shot')
        self._update_ss(self._orders_df)
        # Update to get numbers, just in case
        self._fetch_orders_and_update_panel()

    def _fetch_orders_and_update_panel(self):
        self._orders_df = self._read_ss()
        self.panel_ui.set_orders(self._orders_df)

    @pyqtSlot()
    def _retriever_slot(self):
        """
        Wrapper to call ._read_ss() periodically and update local orders on the
        app
        """
        self._fetch_orders_and_update_panel()

    def _order_interaction(self, row, cb_id: int, cb_checked: bool):
        """
        cb_id is an `int`, but is inverse-searched for the `constants.CBId` equivalent
        """
        if row is not None:
            self._orders_df.loc[row, constants.CBId(cb_id).name] = cb_checked
            self._update_delay_timer.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    reproui_app = ReproUIApp(None)
    reproui_app.show()
    sys.exit(app.exec())
