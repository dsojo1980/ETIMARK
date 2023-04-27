# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_method = fields.Selection(string="Forma de Pago", selection=[("Crédito", "Crédito"),
                                                                         ("Contado", "Contado")])
    observation_note = fields.Text(string="Observación")
    measures_in_cm = fields.Char(string="Medidas en cm")
    raw_material = fields.Char(string="Materia Prima")
    product_id = fields.Many2one(comodel_name='product.product', string="Producto")
    mile_price = fields.Float(string="Precio por Milla", compute='_mile_price', digits='Product Price', store=False)
            
    def _mile_price(self):
        for record in self:
            price = record.price_unit
            total = price * 1000
            record.mile_price = total
            
            
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    product_id = fields.Many2one(comodel_name='product.product', string="Producto")
    mile_price = fields.Float(string="Precio por Milla", compute='_mile_price', digits='Product Price', store=False)
            
    def _mile_price(self):
        for record in self:
            price = record.price_unit
            total = price * 1000
            record.mile_price = total