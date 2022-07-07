"""
     This file is part of ReproUI.

    ReproUI is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    ReproUI is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with ReproUI. If not, see <https://www.gnu.org/licenses/>. 
"""
__author__    = "Echedey Luis Álvaerz"
__copyright__ = "Copyright 2022, Echedey Luis Álvarez"
__credits__   = ["Echedey Luis Álvarez"]
__license__   = "GPL v3"
__version__   = "0.1.0"
__status__    = "Prototype"
__doc__       = "ReproUI is a GUI application designed to aid in the 3D printing service of CREA, UPM. It accesses a Google Spreadsheet and shows a list of pending orders"

import os
import sys
import tomli

import pandas as pd
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSlot
from PyQt6.QtWidgets import *

from googleFlow import googleSpreadSheetInterface
from panelUI import *
import constants
import examples

secretsPath = '.\\secrets'
configFile  = os.path.join(secretsPath, 'config.toml')
dataRange   = 'HojaA!A2:W' # First row is col names

class widgetApp(QMainWindow):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent= parent)

        self.setWindowTitle('ReproUI')

        self.initTimers()

        self.panelUI = panelUI(
            self,
            self.interactionOnOrder
        )
        self.setCentralWidget(self.panelUI)
        self.initSSInterface()
        
        self.getOrdersAndUpdatePanelUI()

    def initTimers(self) -> None:
        self._updateDelayTimer= QTimer(self)
        self._updateDelayTimer.setSingleShot(True)
        self._updateDelayTimer.setTimerType(Qt.TimerType.VeryCoarseTimer)
        self._updateDelayTimer.setInterval(constants.DB_UPDATE_DELAY)
        self._updateDelayTimer.timeout.connect(self.updaterSlot)

        self._retrieveIntervalTimer= QTimer()
        self._retrieveIntervalTimer.setSingleShot(False)
        self._retrieveIntervalTimer.setTimerType(Qt.TimerType.VeryCoarseTimer)
        self._retrieveIntervalTimer.setInterval(constants.DB_RETRIEVE_INTERVAL)
        self._retrieveIntervalTimer.timeout.connect(self.retrieverSlot)

    # Google SpreadSheet functions
    def initSSInterface(self) -> None:
        if( os.path.exists(configFile) and os.path.isfile(configFile) ):
            with open(configFile, 'rb') as cfFile:
                config = tomli.load(cfFile)
        else:
            raise IOError('Configuration file not found')
        self._sSheetInter = googleSpreadSheetInterface(
            secretsPath= secretsPath, 
            spreadSheetId= config['SPREADSHEET_ID']
        )

    def readSS(self) -> pd.DataFrame:
        try:
            ordersRaw = self._sSheetInter.readRange(dataRange)
            ordersDf = pd.DataFrame(
                columns= constants.COLUMN_NAMES,
                # Make sure input is all same length as column names [23]
                data= [ order+[''] if len(order)==22 else order for order in ordersRaw ]
            )
            for booleanColumn in constants.BOOLEAN_COLUMNS:
                ordersDf[booleanColumn] = ordersDf[booleanColumn].map({'TRUE': True, 'FALSE': False, '': False})
            ordersDf = (ordersDf
                .astype(constants.COLUMN_DTYPES)
                .dropna(thresh= 18)
            )
            # Yeah, we shouldn't show all the names. Privacy protection first.
            def privacy_protect_name(name):
                nameSplit = name.split()
                return ' '.join([nameSplit[0]] + [nm[:1].upper()+'.' for nm in nameSplit[1:]])
            ordersDf['NAME'] = ordersDf['NAME'].map(privacy_protect_name)
            return ordersDf

        except TypeError as e:
            print('Error reading orders. Check database integrity.')

    def updateSS(self, ordersDf: pd.DataFrame):
        self._sSheetInter.updateRange(
            range= dataRange,
            values= ordersDf.values.astype(str).tolist()
        )

    # Orders
    @pyqtSlot()
    def updaterSlot(self):
        """
        Wrapper to call .updateSS(orders) with the dataframe argument
        """
        print('Timer shot')
        self.updateSS(self._ordersDf)

    def getOrdersAndUpdatePanelUI(self): # I like to think about this as a self-explanatory name
        self._ordersDf = self.readSS()
        self.panelUI.setOrders(self._ordersDf)

    @pyqtSlot()
    def retrieverSlot(self):
        """
        Wrapper to call .readSS() periodically and update local orders on the app
        """
        self.getOrdersAndUpdatePanelUI()

    def interactionOnOrder(self, row, cbId: CBId, cbChecked: bool):
        if row is not None:
            self._ordersDf.loc[row, constants.CBid2col[cbId]] = cbChecked
            self._updateDelayTimer.start()
        print(f'Row {row}, CB {constants.CBid2col[cbId]} was set to {cbChecked}') # TODO: Remove Debug Line

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widgetApp = widgetApp(None)
    # Open the qss styles file and read in the css-alike styling code
    with open('styles\\styles.qss', 'r') as f:
        style = f.read()
        widgetApp.setStyleSheet(style)
    widgetApp.show()
    sys.exit(app.exec())
