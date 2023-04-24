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
    mile_price = fields.Float(string="Precio por Milla")
    total_price= fields.Float(string="Total x Unidades", compute="_total_x_unidades", store=False)
    
    def _total_x_unidades(self):
        for record in self:
            price = record.product_id.mile_price
            qty = record.product_uom_qty
            total = price * qty
            record.total_price = total
            
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    mile_price = fields.Float(string="Precio por Milla")
    total_price = fields.Float(string="Total x Unidades", compute="_total_x_unidades", store=False)
    
    def _total_x_unidades(self):
        for record in self:
            price = record.product_id.mile_price
            qty = record.product_uom_qty
            total = price * qty
            record.total_price = total