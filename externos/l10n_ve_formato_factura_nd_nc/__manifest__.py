# -*- coding: utf-8 -*-
{
    'name': "Formatos de Factura, NC, ND de forma Libre Etimark",

    'summary': """Formatos de Factura, NC, ND de forma Libre Etimark""",

    'description': """
       Formatos de Factura, NC, ND de forma Libre Etimark.
       Formato de Nota de entrega Etimark.
       Campo de Order de Compra en venta hasta la facturacion..
    """,
    'version': '15.0',
    'author': 'INM & LDR Soluciones Tecnológicas y Empresariales C.A . Ing.Marilynmillan.,' ,
    'category': 'Tools',
    'website': 'http://soluciones-tecno.com/',

    # any module necessary for this one to work correctly
    'depends': ['base','account','ext_extension_nota_debit','sale_to_manufacture'],

    # always loaded
    'data': [
        'formatos/factura_libre.xml',
        'formatos/nota_entrega.xml' ,
        'view/account_move.xml' ,
        'view/account_move_line.xml' ,
        #'view/sale.xml' ,

    ],
    'application': True,
    'active':False,
    'auto_install': False,
}
