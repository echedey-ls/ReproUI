# Some examples to bypass the spreadsheet reader, so we can test offline

from pandas import Timestamp

ordersExamples = {
    '0': {
               'TEMP': Timestamp('2012-05-10T00:00:00'),
              'EMAIL': 'correo@serv.com',
               'NAME': 'Jose María',
                'TEF': '--------1',
          'FILE_LINK': 'about:blank',
            'LAYER_H': '0.3 mm',
           'RIGIDITY': '3',
    'COLOUR_MATERIAL': 'PLA-Negro',
            'COMMENT': 'Comentario 01',
     'SAYS_IS_MEMBER': True,
     'ACCEPTS_PAYING': 'Me doy por enterado de los métodos de pago',
            'PRINTER': 'Impresora?',
      'LOOKUP_MEMBER': True,
             'WEIGHT': 'Peso1?',
               'TIME': 'Tiempo1?',
              'PRICE': 'Precio1?',
           'APPROVED': False,
            'PRINTED': False,
          'PICKED_UP': False,
               'PAID': False,
         'COMPLETION': '0%',
                'REF': 1,
     'REPRO_COMMENTS': ''
    },
    '1': {
               'TEMP': Timestamp('2022-05-10T00:00:00'),
              'EMAIL': 'correo2@serv2.com',
               'NAME': 'Maribí',
                'TEF': '--------2',
          'FILE_LINK': 'about:blank',
            'LAYER_H': '0.2 mm',
           'RIGIDITY': '4',
    'COLOUR_MATERIAL': 'PLA-Blanco',
            'COMMENT': 'Comentario 02',
     'SAYS_IS_MEMBER': False,
     'ACCEPTS_PAYING': 'Me doy por enterado de los métodos de pago',
            'PRINTER': 'Impresora2?',
      'LOOKUP_MEMBER': False,
             'WEIGHT': 'Peso2?',
               'TIME': 'Tiempo2?',
              'PRICE': 'Precio2?',
           'APPROVED': False,
            'PRINTED': False,
          'PICKED_UP': False,
               'PAID': False,
         'COMPLETION': '0%',
                'REF': 2,
     'REPRO_COMMENTS': ''
    }
}
