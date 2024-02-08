# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class ProductCategory(models.Model):
    _inherit = 'product.category'
    

    tipo_producto = fields.Selection([ ('papel', 'Papel'),('tinta', 'Tintas'),('ad', 'Adhesivos'),('otro', 'Otros')])