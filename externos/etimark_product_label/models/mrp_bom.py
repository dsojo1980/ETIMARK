# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class MrpBom(models.Model):

    _inherit = 'mrp.bom'

    product_tmpl_id = fields.Many2one(comodel_name="product.template", 
                                      string='Producto',
                                      check_company=True, 
                                      index=True,
                                      domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", 
                                      required=True)
    raw_material = fields.Char(string='Material', 
                               help="""Refleja el material de la etiqueta que se mostrara al
                               imprimir.""",
                               required=True)
    