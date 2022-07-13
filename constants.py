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
__doc__ = "This file contains constants used in the app"

from enum import IntEnum, unique
from numpy import datetime64

from pandas import Series, Timestamp

# Column tags to rename terrible auto-generated form column titles
COLUMN_NAMES = [
    'TEMP',
    'EMAIL',
    'NAME',
    'TEF',
    'FILE_LINK',
    'LAYER_H',
    'RIGIDITY',
    'COLOUR_MATERIAL',
    'COMMENT',
    'SAYS_IS_MEMBER',
    'ACCEPTS_PAYING',
    'PRINTER',
    'LOOKUP_MEMBER',
    'WEIGHT',
    'TIME',
    'PRICE',
    'APPROVED',
    'PRINTED',
    'PICKED_UP',
    'PAID',
    'COMPLETION',
    'REF',
    'REPRO_COMMENTS'
]
# Columns to convert the dtype
# Commented types is only for reference
# Fetching with valueRenderOption='UNFORMATTED_VALUE'
# already gives expected types
COLUMN_DTYPES = {
    'TEMP': datetime64,
    'EMAIL': None,
    'NAME': None,
    'TEF': object, # Equeals str
    'FILE_LINK': None,
    'LAYER_H': None,
    'RIGIDITY': None, # int,
    'COLOUR_MATERIAL': None,
    'COMMENT': None,
    'SAYS_IS_MEMBER': None, # bool,
    'ACCEPTS_PAYING': None,
    'PRINTER': None,
    'LOOKUP_MEMBER': None, # bool,
    'WEIGHT': None,
    'TIME': None,
    'PRICE': None,
    'APPROVED': None, # bool,
    'PRINTED': None, # bool,
    'PICKED_UP': None, # bool,
    'PAID': None, # bool,
    'COMPLETION': None, # float,
    'REF': None, # int,
    'REPRO_COMMENTS': None
}
# Column A1 notation and name
A1_TO_COLUMN = {
    'TEMP': 'A',
    'EMAIL': 'B',
    'NAME': 'C',
    'TEF': 'D',
    'FILE_LINK': 'E',
    'LAYER_H': 'F',
    'RIGIDITY': 'G',
    'COLOUR_MATERIAL': 'H',
    'COMMENT': 'I',
    'SAYS_IS_MEMBER': 'J',
    'ACCEPTS_PAYING': 'K',
    'PRINTER': 'L',
    'LOOKUP_MEMBER': 'M',
    'WEIGHT': 'N',
    'TIME': 'O',
    'PRICE': 'P',
    'APPROVED': 'Q',
    'PRINTED': 'R',
    'PICKED_UP': 'S',
    'PAID': 'T',
    'COMPLETION': 'U',
    'REF': 'V',
    'REPRO_COMMENTS': 'W'
}
def cols2_a1_notation(col1, col2)  -> str:
    """
    Converts our DF col names to a column range, begins at row 2
    """
    return (
        f'{A1_TO_COLUMN[col1]}2:{A1_TO_COLUMN[col2]}')


@unique
class CBId(IntEnum):
    """
    Enum to interpret checkboxes in _OrderWithControls
    """
    APPROVED = 1
    PRINTED = 2
    PICKED_UP = 3
    PAID = 4

# Placeholder order
ORDER_PLACEHOLDER_SERIES = Series({
    'TEMP': Timestamp('2012-05-10T00:00:00'), # Club birthday, in case you are wondering
    'EMAIL': 'correo@serv.com',
    'NAME': 'Nombre --',
    'TEF': '---------',
    'FILE_LINK': 'about:blank',
    'LAYER_H': '-.- mm',
    'RIGIDITY': '-',
    'COLOUR_MATERIAL': '-- --',
    'COMMENT': 'Comentario --',
    'SAYS_IS_MEMBER': False,
    'ACCEPTS_PAYING': 'Me doy por enterado de los métodos de pago',
    'PRINTER': 'Impresora?',
    'LOOKUP_MEMBER': None,
    'WEIGHT': 'Peso?',
    'TIME': 'Tiempo?',
    'PRICE': 'Precio?',
    'APPROVED': False,
    'PRINTED': False,
    'PICKED_UP': False,
    'PAID': False,
    'COMPLETION': 0.,
    'REF': '----',
    'REPRO_COMMENTS': ''
})
