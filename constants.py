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

# Timers delays
DB_UPDATE_DELAY = 10*1000          # 10 secs
DB_RETRIEVE_INTERVAL = 60*60*1000  # 1 hour

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
# Bool types need special parsing, see next list
COLUMN_DTYPES = {
    'TEMP': datetime64,
    'EMAIL': None,
    'NAME': None,
    'TEF': None,
    'FILE_LINK': None,
    'LAYER_H': None,
    'RIGIDITY': int,
    'COLOUR_MATERIAL': None,
    'COMMENT': None,
    'SAYS_IS_MEMBER': None,  # bool,
    'ACCEPTS_PAYING': None,
    'PRINTER': None,
    'LOOKUP_MEMBER': None,  # bool,
    'WEIGHT': None,
    'TIME': None,
    'PRICE': None,
    'APPROVED': None,  # bool,
    'PRINTED': None,  # bool,
    'PICKED_UP': None,  # bool,
    'PAID': None,  # bool,
    'COMPLETION': None,
    'REF': int,
    'REPRO_COMMENTS': None
}
# Booleans are parsed with a custom parser
BOOLEAN_COLUMNS = [
    'SAYS_IS_MEMBER',
    'LOOKUP_MEMBER',
    'APPROVED',
    'PRINTED',
    'PICKED_UP',
    'PAID'
]


@unique
class CBId(IntEnum):
    """
    Enum to interpret checkboxes in orderWithControls
    """
    APPROVED = 1
    PRINTED = 2
    PICKED_UP = 3
    PAID = 4

# Placeholder order
ORDER_PLACEHOLDER_SERIES = Series({
    'TEMP': Timestamp('2012-05-10T00:00:00'),
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
    'COMPLETION': '0%',
    'REF': '----',
    'REPRO_COMMENTS': ''
})
