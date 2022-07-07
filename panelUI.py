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
__doc__       = "This module provides the orders panel with its interactive elements"

from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import pyqtSlot
from numpy import issubdtype
import pandas as pd

from constants import CBId, ORDER_PLACEHOLDER_SERIES

class panelUI(QWidget):
    def __init__(self, parent: QWidget | None, interactionFunc) -> None:
        """
        interactionFunc is in form f(rowId, CBId, checked)
        """
        super().__init__(parent= parent)
        self._ordersDf = None
        self._interactF = interactionFunc

        self._rowId = None
        self._prevSelected = None

        self.MainVLayout = QVBoxLayout(self)

        ## Scroll Area
        self.ordersScroll = QScrollArea(self)
        self.ordersScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.ordersScroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ordersScroll.setWidgetResizable(True)

        # A QWidget is put into self, the scroll area, which has the vertical layout to be scrolled
        self.columnWidget = QWidget(self)
        self.columnLayout = QVBoxLayout(self.columnWidget)
        self.columnLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.ordersScroll.setWidget(self.columnWidget)

        self.MainVLayout.addWidget(
            self.ordersScroll,
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        ## !Scroll Area
        ## Order & Controls
        self.orderAndControls = orderWithControls(
            self,
            self.interactionWrapper
        )
        self.MainVLayout.addWidget(
            self.orderAndControls,
            QtCore.Qt.AlignmentFlag.AlignBaseline # Or AlignBottom ?
        )
        ## !Order & Controls

    def onOrderClickEvent(self, rowId):
        print(f'LOG: {rowId} was clicked')
        if (self._prevSelected != rowId):
            selectedData = self._ordersDf.loc[rowId]
            self._prevSelected = rowId
            self._rowId = rowId
        else:
            selectedData = ORDER_PLACEHOLDER_SERIES
            self._prevSelected = None
            self._rowId = None
        self.orderAndControls.changeToOrderData(selectedData)

    def setOrders(self, ordersDf: pd.DataFrame):
        # Clear selected order data and save to class
        self.orderAndControls.changeToOrderData(ORDER_PLACEHOLDER_SERIES)
        self._ordersDf = ordersDf
        # Delete all orders
        for widget in self.columnLayout.children():
            self.columnLayout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
        # Create a list of orders
        self.ordersElementsList = [selectableOrder(self, self.onOrderClickEvent, index, order) for index, order in ordersDf.iterrows()]
        # Add new orders
        for selectableOrderElement in self.ordersElementsList:
            self.columnLayout.insertWidget(0, selectableOrderElement)

    @property
    def rowId(self):
        return self._rowId

    def interactionWrapper(self, wId, wChecked):
        self._interactF(self.rowId, wId, wChecked)

class orderBaseElement(QWidget):
    def __init__(self, parent: QWidget | None, properties: pd.Series) -> None:
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
        self.setData(properties)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

    def setData(self, properties: pd.Series):
        self.labelRef.setText(
            f"#{properties['REF']:0>4n}" if issubdtype(type(properties['REF']), int) else f"#{properties['REF']}"
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
    def __init__(self, parent: QWidget | None, reportFunc, rowId: int, properties: pd.Series) -> None:
        """
        Report function: f(rowId)
        """
        super().__init__(parent= parent, properties= properties)
        self._rowId = rowId
        self._reportF = reportFunc
    @property
    def rowId(self):
        return self._rowId
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        # self.setSelected(not self.property('selected'))
        self._reportF(self.rowId)

class orderWithControls(QWidget):
    def __init__(self, parent: QWidget | None, toggledFunc) -> None:
        """
        toggledFunc = f(cbId, cbChecked)
        """
        super().__init__(parent= parent)
        # Tells the painter to paint all the background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.MainVLayout = QVBoxLayout(self)

        self.order = orderBaseElement(
            self,
            ORDER_PLACEHOLDER_SERIES
        )
        self.MainVLayout.addWidget(self.order)
        
        self.interactiveControls = QWidget(self)
        self.interactiveLayout = QHBoxLayout(self.interactiveControls)
        self.CBbuttonGroup = QButtonGroup(self.interactiveControls)
        self.CBbuttonGroup.setExclusive(False)

        self.CBbuttonGroup.idToggled.connect(toggledFunc)

        self._approvedCB = QCheckBox("Aprobado", self)
        self.interactiveLayout.addWidget(self._approvedCB)
        self.CBbuttonGroup.addButton(self._approvedCB, id=CBId.approved)
        self._printedCB = QCheckBox("Impreso", self)
        self.interactiveLayout.addWidget(self._printedCB)
        self.CBbuttonGroup.addButton(self._printedCB, id=CBId.printed)
        self._pickedUpCB = QCheckBox("Recogido", self)
        self.interactiveLayout.addWidget(self._pickedUpCB)
        self.CBbuttonGroup.addButton(self._pickedUpCB, id=CBId.pickedUp)
        self._paidCB = QCheckBox("Pagado", self)
        self.interactiveLayout.addWidget(self._paidCB)
        self.CBbuttonGroup.addButton(self._paidCB, id=CBId.paid)

        self.MainVLayout.addWidget(self.interactiveControls)        

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

    def changeToOrderData(self, order: pd.Series) -> None:
        self.order.setData(order)
        # Disconnect signals before changing CBs statuses
        # Pair of .disconnect / .connect could be used too, but needs the signal handler as argument. Too lazy to try that.
        self.CBbuttonGroup.blockSignals(True)

        self._approvedCB.setChecked(order['APPROVED'])
        self._printedCB.setChecked(order['PRINTED'])
        self._pickedUpCB.setChecked(order['PICKED_UP'])
        self._paidCB.setChecked(order['PAID'])

        # Enable signals
        self.CBbuttonGroup.blockSignals(False)

