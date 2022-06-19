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
__doc__       = "This file contains constants used in the app"

from pandas import Timestamp

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

BOOLEAN_COLUMNS = [
    'SAYS_IS_MEMBER',
    'LOOKUP_MEMBER',
    'APPROVED',
    'PRINTED',
    'PICKED_UP',
    'PAID'
]

INTEGER_COLUMNS = [
    'RIGIDITY',
    'REF'
]

DATETIME_COLUMNS = [
    'TEMP'
]

orderExampleDict = {
               'TEMP': Timestamp('2012-05-10T00:00:00'),
              'EMAIL': 'correo@serv.com',
               'NAME': 'Nombre Cliente',
                'TEF': 'Teléfono',
          'FILE_LINK': 'about:blank',
            'LAYER_H': '0.0 mm',
           'RIGIDITY': 0,
    'COLOUR_MATERIAL': 'Material-Color',
            'COMMENT': 'Comentario Pedido',
     'SAYS_IS_MEMBER': False,
     'ACCEPTS_PAYING': 'Me doy por enterado de los métodos de pago',
            'PRINTER': 'Impresora?',
      'LOOKUP_MEMBER': True,
             'WEIGHT': 'Peso?',
               'TIME': 'Tiempo?',
              'PRICE': 'Precio?',
           'APPROVED': False,
            'PRINTED': False,
          'PICKED_UP': False,
               'PAID': False,
         'COMPLETION': '0%',
                'REF': '¿REF?',
     'REPRO_COMMENTS': ''
}         
