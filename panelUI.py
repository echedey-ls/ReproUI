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
__doc__       = "This module provides the orders panel with it's interactive elements"

import PyQt6
from PyQt6.QtWidgets import *
from PyQt6 import QtCore

class panelUI(QWidget):
    def __init__(self, parent: QWidget | None, orders: dict) -> None:
        super().__init__(parent= parent)
        self.MainColumnLayout = QVBoxLayout(self)
        sections = []
        for order in orders:
            sections.append(sectionElement(self, **order))
            self.MainColumnLayout.addWidget(sections[-1])
        self.setLayout(self.MainColumnLayout)

class sectionElement(QWidget):
    def __init__(self, parent: QWidget | None, **properties) -> None:
        super().__init__(parent= parent)
        # Tells the painter to paint all the background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        # Save properties in case we need them later
        self.properties = properties
        self.MainGridLayout = QGridLayout(self)
        self.labelRef      = QLabel(properties['REF'], self)
        self.labelName     = QLabel(properties['NAME'], self)
        self.labelMember   = QLabel(
            f"Miembro verificado" if(properties['LOOKUP_MEMBER']) else f"Socix sin verificar", 
            self
        )
        self.labelMember.setStyleSheet(
            f"color: {'black' if(properties['LOOKUP_MEMBER']) else 'red'}"
        )
        self.labelComment  = QLabel(properties['COMMENT'])
        self.labelLayerH   = QLabel(f"Altura capa: {properties['LAYER_H']}")
        self.labelRigidity = QLabel(f"Rigidez: {properties['RIGIDITY']}")
        self.labelColour   = QLabel(f"Color: {properties['COLOUR']}")
        self.MainGridLayout.addWidget(self.labelRef, 1, 1)
        self.MainGridLayout.addWidget(self.labelName, 1, 2, 1, 5)
        self.MainGridLayout.addWidget(self.labelMember, 2, 1, 1, 3)
        self.MainGridLayout.addWidget(self.labelComment, 2, 2)
        self.MainGridLayout.addWidget(self.labelLayerH, 3, 1)
        self.MainGridLayout.addWidget(self.labelRigidity, 3, 2)
        self.MainGridLayout.addWidget(self.labelColour, 3, 3)
        self.setStyleSheet("""
            background-color: cyan;
        """)
        self.setLayout(self.MainGridLayout)
        

