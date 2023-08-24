# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from odoo import api, fields, models, _
from odoo import tools
from odoo.fields import Command
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date
import datetime
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_method = fields.Selection(string="Forma de Pago", selection=[("Crédito", "Crédito"),
                                                                         ("Contado", "Contado")])
    measures_in_cm = fields.Char(string="Medidas en cm")
    raw_material = fields.Char(string="Materia Prima")
            
            
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    product_id = fields.Many2one(comodel_name='product.product', string="Producto")
    mile_price = fields.Float(string="Precio por Millar Bs.", compute='_mile_price_bs', digits=(12,2), store=False)
    mile_price_usd = fields.Float(string="Precio por Millar $", 
                                  digits=(12,2),
                                  compute='_mile_price_usd',
                                  store=False)
    
    @api.onchange('discount')
    def _mile_price_usd(self):
        for record in self:
            price = record.price_unit_rate if self.company_id.currency_id.id==self.order_id.pricelist_id.currency_id.id else record.price_unit_rate*record.order_id.inverse_rate
            dis = record.discount
            if dis == 0:
                total = price * 1000
                record.mile_price_usd = total
            if dis > 0:
                price_mil = price * 1000
                discount = price_mil * (dis / 100)
                total = price_mil - discount
                record.mile_price_usd = total 

    @api.onchange('discount')
    def _mile_price_bs(self):
        for record in self:
            price = record.price_unit if self.company_id.currency_id.id==self.order_id.pricelist_id.currency_id.id else record.price_unit*self.order_id.rate
            dis = record.discount
            if dis == 0:
                total = price * 1000
                record.mile_price = total
            if dis > 0:
                price_mil = price * 1000
                discount = price_mil * (dis / 100)
                total = price_mil - discount
                record.mile_price = total

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res.update({'sol_id' : self.id})
        return res