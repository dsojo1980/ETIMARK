# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class MrpProduction(models.Model):

    _inherit = 'mrp.production'

    production_date = fields.Datetime(string="Fecha de Producción", 
                                      default=datetime.today(),
                                      help="""Fecha que refleja el día de impresión o 
                                      fabricación del producto terminado""",
                                      required=True)
    material_contains = fields.Char(string="Contiene",
                                    help="""Indica la cantidad de rollos que se imprimieron
                                    en la orden de fabricación""",
                                    required=True)
    quantity = fields.Char(string="Cantidad",
                           help="""Muestra la cantidad de unidades que representan
                           todos los rollos registrados en el campo "Contiene" """,
                           required=True)
    is_approved = fields.Boolean(string="Aprobado",
                                 help="""Indica si la etiqueta está aprobado es verdadero 
                                 o fallido cuando es falso""")
    revision_date = fields.Datetime(string="Fecha de Revisión", 
                                    default=datetime.today(),
                                    help="""Muestra la fecha de impresión o fabricación
                                    del producto terminado""",
                                    required=True)
    
    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        if self.state == 'confirmed':
            self.state_update_production_indicators()
            self.onchange_shrinkage_process()
            self.is_approved == True
        return res
