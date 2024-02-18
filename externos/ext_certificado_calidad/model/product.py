# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    

    espesor = fields.Char()
    gramaje = fields.Char()
    adhesivo = fields.Char()

    def write(self,vals):
        super().write(vals)
        lista=self.env['product.product'].search([('product_tmpl_id','=',self.id)])
        if lista:
            for det in lista:
                det.espesor=self.espesor
                det.gramaje=self.gramaje
                det.adhesivo=self.adhesivo

class ProductTemplate(models.Model):
    _inherit = 'product.product'
    

    espesor = fields.Char()
    gramaje = fields.Char()
    adhesivo = fields.Char()