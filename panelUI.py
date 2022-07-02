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
from PyQt6 import QtCore, QtGui

from constants import orderExampleDict

class panelUI(QWidget):
    def __init__(self, parent: QWidget | None, ordersDict: dict[dict]) -> None:
        super().__init__(parent= parent)
        self._ordersDict = ordersDict
        self._prevSelected = None

        self.MainVLayout = QVBoxLayout(self)

        self.ordersElementsList = [selectableOrder(self, self.onOrderEvent, rowId, **order) for rowId, order in ordersDict.items()]

        ## Scroll Area
        self.ordersScroll = QScrollArea(self)
        self.ordersScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ordersScroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ordersScroll.setWidgetResizable(True)

        # A QWidget is put into self, the scroll area, which has the vertical layout to be scrolled
        self.columnWidget = QWidget(self)
        self.columnLayout = QVBoxLayout(self.columnWidget)
        self.columnLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        
        for selectableOrderElement in self.ordersElementsList:
            self.columnLayout.insertWidget(0, selectableOrderElement)

        self.ordersScroll.setWidget(self.columnWidget)
        ## !Scroll Area

        self.MainVLayout.addWidget(
            self.ordersScroll,
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.orderAndControls = orderWithControls(self)
        self.MainVLayout.addWidget(
            self.orderAndControls,
            QtCore.Qt.AlignmentFlag.AlignBaseline # Or AlignBottom ?
        )

    def onOrderEvent(self, rowId):
        print(f'LOG: {rowId} was clicked')
        if (self._prevSelected != rowId):
            selectedData = self._ordersDict[rowId]
            self._prevSelected = rowId
        else:
            selectedData = orderExampleDict
            self._prevSelected = None
        self.orderAndControls.changeToOrderData(selectedData)
        pass

class orderBaseElement(QWidget):
    def __init__(self, parent: QWidget | None, **properties: dict) -> None:
        super().__init__(parent= parent)

        # TODO: remove if unused
        # Save properties in case we need them later
        self._properties = properties

        # Tells the painter to paint all the background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.MainGridLayout = QGridLayout(self)

        # Create labels, apply styles and add to self
        self.labelRef      = QLabel(self)
        self.labelName     = QLabel(self)
        self.labelMember   = QLabel(self)
        self.labelComment  = QLabel(self)
        self.labelLayerH   = QLabel(self)
        self.labelRigidity = QLabel(self)
        self.labelMaterial = QLabel(self)
        self.labelRef.setStyleSheet(
            "font-weight: bold;"
            "font-size: 18px;"
        )
        self.labelName.setStyleSheet(
            "font-size: 18px;"
        )
        self.MainGridLayout.addWidget(self.labelRef, 1, 1)
        self.MainGridLayout.addWidget(self.labelName, 1, 2, 1, 2)
        self.MainGridLayout.addWidget(self.labelMember, 2, 1)
        self.MainGridLayout.addWidget(self.labelComment, 2, 2, 1, 2)
        self.MainGridLayout.addWidget(self.labelLayerH, 3, 1)
        self.MainGridLayout.addWidget(self.labelRigidity, 3, 2)
        self.MainGridLayout.addWidget(self.labelMaterial, 3, 3)

        # Put label data
        self.setData(**properties)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

    def setData(self, **properties: dict):
        self.labelRef.setText(
            f"#{properties['REF']:0>4n}" if type(properties['REF']) is int else f"#{properties['REF']}"
        )
        self.labelName.setText(
            properties['NAME']
        )
        self.labelMember.setText(
            f"Contrastar miembro" if(properties['LOOKUP_MEMBER'] is None) else
            f"Miembro verificado" if(properties['LOOKUP_MEMBER']) else f"No verificado"
        )
        self.labelMember.setStyleSheet(
            f"color: {'red' if(not properties['LOOKUP_MEMBER']) else 'black'}"
        )
        self.labelComment.setText(
            properties['COMMENT']
        )
        self.labelLayerH.setText(
            f"Altura capa: {properties['LAYER_H']}"
        )
        self.labelRigidity.setText(
            f"Rigidez: {properties['RIGIDITY']}/5"
        )
        self.labelMaterial.setText(
            f"Material: {properties['COLOUR_MATERIAL']}"
        )

class selectableOrder(orderBaseElement):
    def __init__(self, parent: QWidget | None, reportFunc, rowId, **properties: dict) -> None:
        """
        Report function: f(rowId)
        """
        super().__init__(parent= parent, rowId= rowId, **properties)
        self._rowId = rowId
        self._reportF = reportFunc
    @property
    def rowId(self):
        return self._rowId
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        # self.setSelected(not self.property('selected'))
        self._reportF(self.rowId)

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
        self.MainVLayout.addWidget(self.order)
        
        self.interactiveControls = QWidget(self)
        self.interactiveLayout = QHBoxLayout(self.interactiveControls)

        self._approvedCB = QCheckBox("Aprobado", self)
        self.interactiveLayout.addWidget(self._approvedCB)
        self._printedCB = QCheckBox("Impreso", self)
        self.interactiveLayout.addWidget(self._printedCB)
        self._pickedUpCB = QCheckBox("Recogido", self)
        self.interactiveLayout.addWidget(self._pickedUpCB)
        self._paidCB = QCheckBox("Pagado", self)
        self.interactiveLayout.addWidget(self._paidCB)

        self.MainVLayout.addWidget(self.interactiveControls)        

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

    def changeToOrderData(self, orderDict: dict | None) -> None:
        self.order.setData(**orderDict)
        self._approvedCB.setChecked(orderDict['APPROVED'])
        self._printedCB.setChecked(orderDict['PRINTED'])
        self._pickedUpCB.setChecked(orderDict['PICKED_UP'])
        self._paidCB.setChecked(orderDict['PAID'])

