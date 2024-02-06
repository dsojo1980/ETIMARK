# -*- coding: utf-8 -*-
{
    'name': "Formatos de Certificado de Calidad",

    'summary': """Formatos de Certificado de Calidad Etimark""",

    'description': """
       Formatos de Certificado de Calidad Etimark.
       FFormatos de Certificado de Calidad Etimark...
    """,
    'version': '15.0',
    'author': 'Darrell Sojo,' ,
    'category': 'Tools',
    'website': 'dsojo.tanfe@gmail.com',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_to_manufacture','mrp'],

    # always loaded
    'data': [
        #'formatos/factura_libre.xml',
        #'formatos/nota_entrega.xml' ,
        'view/m_production_view.xml' ,
        'view/report_certification.xml' ,
        #'view/sale.xml' ,

    ],
    'application': True,
    'active':False,
    'auto_install': False,
}
