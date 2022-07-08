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
__version__ = "0.1.0"
__status__ = "Prototype"
__doc__ = "This module provides the orders panel with its interactive elements"

from PyQt6.QtWidgets import (QWidget, QScrollArea, QVBoxLayout, QHBoxLayout,
                             QLabel, QGridLayout, QCheckBox, QSizePolicy,
                             QButtonGroup)
from PyQt6 import QtCore, QtGui
from numpy import issubdtype
import pandas as pd

from constants import CBId, ORDER_PLACEHOLDER_SERIES


class PanelUI(QWidget):
    def __init__(self, parent: QWidget | None, interactionFunc) -> None:
        """
        interactionFunc is in form f(row_id, CBId, checked)
        """
        super().__init__(parent=parent)
        self._orders_df = None
        self._interact_func = interactionFunc

        self._row_id = None
        self._prev_selected = None

        self.orders_elements_list = None

        self.main_v_layout = QVBoxLayout(self)

        # Scroll Area
        self.orders_scroll = QScrollArea(self)
        self.orders_scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.orders_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.orders_scroll.setWidgetResizable(True)

        # A QWidget is put into self, the scroll area, which has the vertical
        # layout to be scrolled
        self.column_wdgt = QWidget(self)
        self.column_lyt = QVBoxLayout(self.column_wdgt)
        self.column_lyt.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.orders_scroll.setWidget(self.column_wdgt)

        self.main_v_layout.addWidget(
            self.orders_scroll,
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        # !Scroll Area
        # Order & Controls
        self.orders_and_controls = OrderWithControls(
            self,
            self.interaction_wrapper
        )
        self.main_v_layout.addWidget(
            self.orders_and_controls,
            QtCore.Qt.AlignmentFlag.AlignBaseline  # Or AlignBottom ?
        )
        # !Order & Controls

    def on_order_click_event(self, row_id):
        print(f'LOG: {row_id} was clicked')
        if self._prev_selected != row_id:
            selected_data = self._orders_df.loc[row_id]
            self._prev_selected = row_id
            self._row_id = row_id
        else:
            selected_data = ORDER_PLACEHOLDER_SERIES
            self._prev_selected = None
            self._row_id = None
        self.orders_and_controls.change_order(selected_data)

    def set_orders(self, orders_df: pd.DataFrame):
        # Clear selected order data and save to class
        self.orders_and_controls.change_order(ORDER_PLACEHOLDER_SERIES)
        self._orders_df = orders_df
        # Delete all orders
        for widget in self.column_lyt.children():
            self.column_lyt.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
        # Create a list of orders
        self.orders_elements_list = [
            SelectableOrder(self, self.on_order_click_event, index, order)
            for index, order in orders_df.iterrows()]
        # Add new orders
        for selectable_order in self.orders_elements_list:
            self.column_lyt.insertWidget(0, selectable_order)

    @property
    def row_id(self):
        return self._row_id

    def interaction_wrapper(self, w_id, w_checked):
        self._interact_func(self.row_id, w_id, w_checked)


class OrderBaseElement(QWidget):
    def __init__(self, parent: QWidget | None, properties: pd.Series) -> None:
        super().__init__(parent=parent)

        # Tells the painter to paint all the background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.main_grid_lyt = QGridLayout(self)

        # Create labels, apply styles and add to self
        self.label_ref = QLabel(self)
        self.label_name = QLabel(self)
        self.label_member = QLabel(self)
        self.label_comment = QLabel(self)
        self.label_layer_h = QLabel(self)
        self.label_rigidity = QLabel(self)
        self.label_material = QLabel(self)
        self.label_ref.setStyleSheet(
            "font-weight: bold;"
            "font-size: 18px;"
        )
        self.label_name.setStyleSheet(
            "font-size: 18px;"
        )
        self.main_grid_lyt.addWidget(self.label_ref, 1, 1)
        self.main_grid_lyt.addWidget(self.label_name, 1, 2, 1, 2)
        self.main_grid_lyt.addWidget(self.label_member, 2, 1)
        self.main_grid_lyt.addWidget(self.label_comment, 2, 2, 1, 2)
        self.main_grid_lyt.addWidget(self.label_layer_h, 3, 1)
        self.main_grid_lyt.addWidget(self.label_rigidity, 3, 2)
        self.main_grid_lyt.addWidget(self.label_material, 3, 3)

        # Put label data
        self.set_data(properties)

        self.setSizePolicy(QSizePolicy.Policy.Minimum,
                           QSizePolicy.Policy.Maximum)

    def set_data(self, properties: pd.Series):
        self.label_ref.setText(
            f"#{properties['REF']:0>4n}"
            if issubdtype(type(properties['REF']), int)
            else f"#{properties['REF']}"
        )
        self.label_name.setText(
            properties['NAME']
        )
        self.label_member.setText(
            "Contrastar miembro" if(properties['LOOKUP_MEMBER'] is None) else
            "Miembro verificado" if(properties['LOOKUP_MEMBER']) else
            "Sin verificación"
        )
        self.label_member.setStyleSheet(
            f"color: {'red' if(not properties['LOOKUP_MEMBER']) else 'black'}"
        )
        self.label_comment.setText(
            properties['COMMENT']
        )
        self.label_layer_h.setText(
            f"Altura capa: {properties['LAYER_H']}"
        )
        self.label_rigidity.setText(
            f"Rigidez: {properties['RIGIDITY']}/5"
        )
        self.label_material.setText(
            f"Material: {properties['COLOUR_MATERIAL']}"
        )


class SelectableOrder(OrderBaseElement):
    def __init__(self, parent: QWidget | None, report_fnc, row_id: int,
                 properties: pd.Series) -> None:
        """
        Report function: f(row_id)
        """
        super().__init__(parent=parent, properties=properties)
        self._row_id = row_id
        self._report_fnc = report_fnc

    @property
    def row_id(self):
        """Returns id given to the order"""
        return self._row_id

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:  # pylint: disable=invalid-name, missing-function-docstring
        self._report_fnc(self.row_id)


class OrderWithControls(QWidget):
    def __init__(self, parent: QWidget | None, toggledFunc) -> None:
        """
        toggledFunc = f(cbId, cbChecked)
        """
        super().__init__(parent=parent)
        # Tells the painter to paint all the background
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.main_v_layout = QVBoxLayout(self)

        self.order = OrderBaseElement(
            self,
            ORDER_PLACEHOLDER_SERIES
        )
        self.main_v_layout.addWidget(self.order)

        self.interactive_controls = QWidget(self)
        self.interactive_layout = QHBoxLayout(self.interactive_controls)
        self.cb_button_group = QButtonGroup(self.interactive_controls)
        self.cb_button_group.setExclusive(False)

        self.cb_button_group.idToggled.connect(toggledFunc)

        self._approved_cb = QCheckBox("Aprobado", self)
        self._printed_cb = QCheckBox("Impreso", self)
        self._pickedup_cb = QCheckBox("Recogido", self)
        self._paid_cb = QCheckBox("Pagado", self)
        self.interactive_layout.addWidget(self._approved_cb)
        self.interactive_layout.addWidget(self._printed_cb)
        self.interactive_layout.addWidget(self._pickedup_cb)
        self.interactive_layout.addWidget(self._paid_cb)
        self.cb_button_group.addButton(self._approved_cb, id=CBId.APPROVED)
        self.cb_button_group.addButton(self._printed_cb, id=CBId.PRINTED)
        self.cb_button_group.addButton(self._pickedup_cb, id=CBId.PICKED_UP)
        self.cb_button_group.addButton(self._paid_cb, id=CBId.PAID)

        self.main_v_layout.addWidget(self.interactive_controls)

        self.setSizePolicy(QSizePolicy.Policy.Minimum,
                           QSizePolicy.Policy.Maximum)

    def change_order(self, order: pd.Series) -> None:
        self.order.set_data(order)
        # Disconnect signals before changing CBs statuses
        # Pair of .disconnect / .connect could be used too,
        # but needs the signal handler as argument. This works just well.
        self.cb_button_group.blockSignals(True)

        self._approved_cb.setChecked(order['APPROVED'])
        self._printed_cb.setChecked(order['PRINTED'])
        self._pickedup_cb.setChecked(order['PICKED_UP'])
        self._paid_cb.setChecked(order['PAID'])

        # Enable signals
        self.cb_button_group.blockSignals(False)
