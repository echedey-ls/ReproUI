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

from PyQt6.QtWidgets import *
from PyQt6 import QtCore

from constants import orderExampleDict

class panelUI(QWidget):
    def __init__(self, parent: QWidget | None, ordersDict: dict) -> None:
        super().__init__(parent= parent)
        self.MainVLayout = QVBoxLayout(self)

        self.scrollableOrders = scrollableOrders(self, ordersDict)
        self.MainVLayout.addWidget(
            self.scrollableOrders,
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.orderAndControls = orderWithControls(self)
        self.MainVLayout.addWidget(
            self.orderAndControls,
            QtCore.Qt.AlignmentFlag.AlignBaseline # Or AlignBottom ?
        )
        self.setLayout(self.MainVLayout)

class scrollableOrders(QScrollArea):
    def __init__(self, parent: QWidget | None, orders: dict) -> None:
        super().__init__(parent= parent)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        # A QWidget is put into self, the scroll area, which has the vertical layout to be scrolled
        self.columnWidget = QWidget()
        self.columnLayout = QVBoxLayout()
        self.columnLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        
        for order in orders:
            self.columnLayout.insertWidget(0, orderBaseElement(self, **order))
        self.columnWidget.setLayout(self.columnLayout)
        self.setWidget(self.columnWidget)

class orderBaseElement(QWidget):
    def __init__(self, parent: QWidget | None, **properties) -> None:
        super().__init__(parent= parent)
        # Save properties in case we need them later
        self._properties = properties

        # Tells the painter to paint all the background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.MainGridLayout = QGridLayout(self)

        self.labelRef      = QLabel(
            f"#{properties['REF']:0>4n}" if type(properties['REF']) is int else f"#{properties['REF']}",
            self
        )
        self.labelRef.setStyleSheet(
            "font-weight: bold;"
            "font-size: 18px;"
        )
        self.labelName     = QLabel(
            properties['NAME'],
            self
        )
        self.labelName.setStyleSheet(
            "font-size: 18px;"
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
            f"Rigidez: {properties['RIGIDITY']}/5",
            self
        )
        self.labelMaterial = QLabel(
            f"Material: {properties['COLOUR_MATERIAL']}",
            self
        )

        self.MainGridLayout.addWidget(self.labelRef, 1, 1)
        self.MainGridLayout.addWidget(self.labelName, 1, 2, 1, 2)
        self.MainGridLayout.addWidget(self.labelMember, 2, 1)
        self.MainGridLayout.addWidget(self.labelComment, 2, 2, 1, 2)
        self.MainGridLayout.addWidget(self.labelLayerH, 3, 1)
        self.MainGridLayout.addWidget(self.labelRigidity, 3, 2)
        self.MainGridLayout.addWidget(self.labelMaterial, 3, 3)
        self.setStyleSheet("""
            background-color: #82caaf;
        """)
        self.setLayout(self.MainGridLayout)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

class orderWithControls(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent= parent)
        # Tells the painter to paint all the background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.MainVLayout = QVBoxLayout(self)

        self.order = orderBaseElement(
            self,
            **orderExampleDict
        )
        
        self.interactiveLayout = QHBoxLayout(self)

        self._approvedCB = QCheckBox("Aprobado", self)
        self.interactiveLayout.addWidget(self._approvedCB)

        self.MainVLayout.addWidget(self.order)
        self.MainVLayout.addLayout(self.interactiveLayout)

        self.setStyleSheet("""
            background-color: #b676b1;
        """)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

    def changeToOrderData(self, orderDict: dict | None) -> None:
        self.order = orderBaseElement(
            self,
            orderDict if orderDict is None else orderExampleDict
        )
