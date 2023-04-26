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
    order_line_id = fields.Many2one(comodel_name='sale.order.line', string="Linea de Pedido")
    mile_price = fields.Float(string="Precio por Milla", digits=(12,2), related='order_line_id.mile_price', store=True)
    
class ProductProduct(models.Model):
    _inherit = "product.product"

    payment_method = fields.Selection(string="Forma de Pago", selection=[("Crédito", "Crédito"),
                                                                         ("Contado", "Contado")])
    quotation = fields.Char(string="Cotización")
    observation_note = fields.Text(string="Observación")
    measures_in_cm = fields.Char(string="Medidas en cm")
    raw_material = fields.Char(string="Materia Prima")
    order_line_id = fields.Many2one(comodel_name='sale.order.line', string="Linea de Pedido")
    mile_price = fields.Float(string="Precio por Milla", digits=(12,2), related='order_line_id.mile_price', store=True)
    