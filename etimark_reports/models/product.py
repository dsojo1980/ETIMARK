# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    payment_method = fields.Selection(string="Forma de Pago", selection=[("Crédito", "Crédito"),
                                                                         ("Contado", "Contado")])
    quotation = fields.Char(string="Cotización")
    observation_note = fields.Text(string="Observación")
    measures_in_cm = fields.Char(string="Medidas en cm")
    raw_material = fields.Char(string="Materia Prima")
    mile_price = fields.Float(string="Precio por Milla", compute='_mile_price', digits=(12,2), store=False)
            
    def _mile_price(self):
        for record in self:
            price = record.list_price_usd
            total = price * 1000
            record.mile_price = total
            
            
    
class ProductProduct(models.Model):
    _inherit = "product.product"

    payment_method = fields.Selection(string="Forma de Pago", selection=[("Crédito", "Crédito"),
                                                                         ("Contado", "Contado")])
    quotation = fields.Char(string="Cotización")
    observation_note = fields.Text(string="Observación")
    measures_in_cm = fields.Char(string="Medidas en cm")
    raw_material = fields.Char(string="Materia Prima")
    mile_price = fields.Float(string="Precio por Milla", compute='_mile_price', digits=(12,2), store=False)
            
    def _mile_price(self):
        for record in self:
            price = record.list_price_usd
            total = price * 1000
            record.mile_price = total