# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Reportes de Etimark",
    "summary": """
        Formatos de Compras / Venta de la empresa """,
    'description': """
        Formatos de las cotizaciones de Compras y Venta de la empresa Etimark C.A. 
    """,
    "version": "16.0.1.0.0",
    "author": """Ing. José Antonio Martínez""",
    "license": "AGPL-3",
    "depends": ["base",
                "purchase",
                "sale",
                "stock",
                "l10n_ve_currency_rate",
                ],
    "data": [
        'views/purchase_order_templates.xml',
        'views/res_partner_view.xml',
        'views/purchase_order_view.xml',
        'views/product_template_view.xml',
        'views/sale_order_view.xml',
        'views/sale_order_template.xml',
    ]
    
}
