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
from numpy import datetime64
import tomli

import pandas as pd
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *

from googleFlow import googleSpreadSheetInterface
from panelUI import panelUI
import constants

secretsPath = '.\\secrets'
configFile  = os.path.join(secretsPath, 'config.toml')
dataRange   = 'HojaA!A1:W'

class widgetApp(QMainWindow):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent= parent)

        self.initSSInterface()

        
        ordersDict = self.readSS().to_dict('records')
        self.panelUI = panelUI(self, ordersDict)
        self.initUI()

    def initUI(self) -> None:
        self.setCentralWidget(self.panelUI)
        pass
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
        ordersRaw = self._sSheetInter.readRange(dataRange)
        ordersDf = pd.DataFrame(
            columns= constants.COLUMN_NAMES,
            # Make sure input is all same length as column names
            data= [ order+[''] if len(order)==22 else order for order in ordersRaw[1:] ]
        )
        for booleanColumn in constants.BOOLEAN_COLUMNS:
            ordersDf[booleanColumn] = ordersDf[booleanColumn].map({'TRUE': True, 'FALSE': False, '': False})
        for integerColumn in constants.INTEGER_COLUMNS:
            ordersDf[integerColumn] = ordersDf[integerColumn].astype(int)
        for datetimeDolumn in constants.DATETIME_COLUMNS:
            ordersDf[datetimeDolumn] = ordersDf[datetimeDolumn].astype(datetime64)
        return ordersDf

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widgetApp = widgetApp(None)
    widgetApp.show()
    sys.exit(app.exec())
