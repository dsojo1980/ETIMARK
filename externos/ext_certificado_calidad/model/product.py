# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    

    espesor = fields.Char()
    gramaje = fields.Char()
    adhesivo = fields.Char()

class ProductTemplate(models.Model):
    _inherit = 'product.product'
    

    espesor = fields.Char()
    gramaje = fields.Char()
    adhesivo = fields.Char()