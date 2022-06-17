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
        # Save properties in case we need them later
        self.properties = properties
        # Tells the painter to paint all the background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.MainLayout = QVBoxLayout(self)

        self.UpperRow   = QHBoxLayout(self)
        self.MiddleRow  = QHBoxLayout(self)
        self.LowerRow   = QHBoxLayout(self)

        self.labelRef      = QLabel(
            properties['REF'],
            self
        )
        self.labelName     = QLabel(
            properties['NAME'],
            self
        )
        self.labelMember   = QLabel(
            f"Miembro verificado" if(properties['LOOKUP_MEMBER']) else f"Socix sin verificar", 
            self
        )
        self.labelMember.setStyleSheet(
            f"color: {'black' if(properties['LOOKUP_MEMBER']) else 'red'}"
        )
        self.labelComment  = QLabel(
            properties['COMMENT'],
            self
        )
        self.labelLayerH   = QLabel(
            f"Altura capa: {properties['LAYER_H']}",
            self
        )
        self.labelRigidity = QLabel(
            f"Rigidez: {properties['RIGIDITY']}",
            self
        )
        # self.labelRigidity.setStyleSheet(
        #     f
        # )
        self.labelColour   = QLabel(
            f"Color: {properties['COLOUR']}",
            self
        )

        self.UpperRow.addWidget(self.labelRef, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.UpperRow.addWidget(self.labelName, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.MiddleRow.addWidget(self.labelComment)

        self.LowerRow.addWidget(self.labelLayerH)
        self.LowerRow.addWidget(self.labelRigidity)
        self.LowerRow.addWidget(self.labelColour)
        self.LowerRow.addWidget(self.labelMember)

        self.MainLayout.addLayout(self.UpperRow)
        self.MainLayout.addLayout(self.MiddleRow)
        self.MainLayout.addLayout(self.LowerRow)

        self.setStyleSheet("""
            background-color: cyan;
        """)
        self.setLayout(self.MainLayout)
