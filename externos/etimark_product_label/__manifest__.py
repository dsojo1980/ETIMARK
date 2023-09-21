# -*- coding: utf-8 -*-
{
    'name': "Etiquetas de Etimark",

    'summary': """
        Formatos de Etiquetas para los productos de Etimark""",

    'description': """
        Formatos de las etiquetas de los productos de la empresa ETIMARK C.A.
        Colaborador: Ing. José Antonio Martínez
    """,

    'author': 'INM&LDR Soluciones Tecnologicas',
    'maintainer': 'INM&LDR Soluciones Tecnologicas',
    'contribuitors': 'Ing. José Martínez [jamp1495@gmail.com, https://github.com/jamp1495]',
    'license': 'LGPL-3',
    'version': '15.0.1',
    'category': 'Etimark',
    'depends': [
        'base',
        'product',
        'mrp',
        'sale_to_manufacture',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_production_view.xml',
        'views/mrp_bom_view.xml',
        'views/mrp_storage_conditions_view.xml',
        'views/mrp_manual_operations_view.xml',
        'reports/product_label_reports.xml',
        'reports/product_label_template.xml',
    ],
}
