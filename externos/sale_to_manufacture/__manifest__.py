{
    "name": "From Sale to Manufacture",
    "version": "15.0.01",
    "author": "Holos",
    'contributors': "Oscar Mora <oscar1596mora@gmail.com>",
    'maintainer': "Oscar Mora <oscar1596mora@gmail.com>",
    'website': '',
    "category": "Fabricación",
    "description": """
            """,
    "depends": ['base','mrp', 'sale'],
    "data": [
        'security/ir.model.access.csv',
        'report/paperformat.xml',
        'report/ir_action_report.xml',
        'views/mrp_production_view.xml',
        'views/maintenance_equipment_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/report_production_indicators_view.xml',
        'views/mrp_workcenter_view.xml',
        'views/report_indicator.xml',
        'wizard/wizard_report_indicator_view.xml'

    ],
    'license': "OPL-1",
    'installable': True,
    'application': False,
}
