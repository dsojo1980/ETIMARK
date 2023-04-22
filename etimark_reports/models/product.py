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
    mile_price = fields.Float(string="Precio por Milla", digits='Product Price', required=True, default=0.0)
    total_price= fields.Float(string="Total x Unidades", compute="_total_x_unidades", store=False)
    
    def _total_x_unidades(self):
        for record in self:
            price = record.mile_price
            qty = record.qty_available
            total = price * qty
            record.total_price = total
    
class ProductProduct(models.Model):
    _inherit = "product.product"

    payment_method = fields.Selection(string="Forma de Pago", selection=[("Crédito", "Crédito"),
                                                                         ("Contado", "Contado")])
    quotation = fields.Char(string="Cotización")
    observation_note = fields.Text(string="Observación")
    measures_in_cm = fields.Char(string="Medidas en cm")
    raw_material = fields.Char(string="Materia Prima")
    mile_price = fields.Float(string="Precio por Milla", digits='Product Price', required=True, default=0.0)
    total_price= fields.Float(string="Total x Unidades", compute="_total_x_unidades", store=False)
    
    def _total_x_unidades(self):
        for record in self:
            price = record.mile_price
            qty = record.qty_available
            total = price * qty
            record.total_price = total
    