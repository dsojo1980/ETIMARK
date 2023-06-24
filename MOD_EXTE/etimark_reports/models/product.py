# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date
from odoo.tools import format_amount

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _set_currency_usd_id(self):
        usd = self.env.ref("base.USD")
        return usd
    
    payment_method = fields.Selection(string="Forma de Pago", selection=[("Crédito", "Crédito"),
                                                                         ("Contado", "Contado")])
    quotation = fields.Char(string="Cotización")
    observation_note = fields.Text(string="Observación")
    measures_in_cm = fields.Char(string="Medidas en cm")
    raw_material = fields.Char(string="Materia Prima")
    mile_price_usd = fields.Float(string="Precio por Millar $", compute='_mile_price_usd', digits=(12,2), store=False)
    mile_price = fields.Float(string="Precio por Millar Bs.", compute='_mile_price', digits=(12,2), store=False)
    currency_usd_id = fields.Many2one(comodel_name="res.currency", string="USD", default=_set_currency_usd_id)
    mile_standard_price_usd = fields.Float(string="Costo por Millar $", digits=(12,2), compute='_mile_standard_price_usd', store=False)
    mile_standard_price_bs = fields.Float(string="Costo por Millar Bs.", digits=(12,2), compute='_mile_standard_price_bs', store=False)
    tax_string_usd = fields.Char(string="Impuesto Producto $",
                                 compute='_compute_tax_string_usd')       
            
    @api.onchange("list_price_usd")
    def _mile_price_usd(self):
        for record in self:
            price_usd = record.list_price_usd
            total_usd = price_usd * 1000
            record.mile_price_usd = total_usd
            
    @api.onchange("list_price")
    def _mile_price(self):
        for record in self:
            price_bs = record.list_price
            total_bs = price_bs * 1000
            record.mile_price = total_bs

    @api.onchange("mile_price_usd")
    def onchange_mile_price_bs_rate(self):
        new_mile_price = 0.0
        rate = self.env["res.currency.rate"].search([("name", "<=", date.today()), 
                                                     ("currency_id", "=", self.currency_usd_id.id)], limit=1).inverse_company_rate
        if rate: 
            new_mile_price += self.mile_price_usd * rate 
        else:
            new_mile_price += self.mile_price_usd * 1
        self.mile_price = new_mile_price
        for item in self.product_variant_ids:
            item.mile_price = new_mile_price

    @api.onchange("cost_usd")
    def _mile_standard_price_usd(self):
        for record in self:
            standard_price_usd = record.cost_usd
            total_usd = standard_price_usd * 1000
            record.mile_standard_price_usd = total_usd

    @api.onchange("standard_price")
    def _mile_standard_price_bs(self):
        for record in self:
            standard_price_bs = record.standard_price
            total_usd = standard_price_bs * 1000
            record.mile_standard_price_bs = total_usd

    @api.onchange("mile_standard_price_usd")
    def onchange_mile_standard_price_bs_rate(self):
        new_mile_price = 0.0
        rate = self.env["res.currency.rate"].search([("name", "<=", date.today()), 
                                                     ("currency_id", "=", self.currency_usd_id.id)], limit=1).inverse_company_rate
        if rate: 
            new_mile_price += self.mile_standard_price_usd * rate 
        else:
            new_mile_price += self.mile_standard_price_usd * 1
        self.mile_standard_price_bs = new_mile_price
        for item in self.product_variant_ids:
            item.mile_standard_price_bs = new_mile_price
            
    @api.onchange('cost_usd')
    def onchange_cost_bs(self):
        new_price = 0.0
        rate = self.env['res.currency.rate'].search([
            ('name', '<=', date.today()), ('currency_id', '=', self.currency_usd_id.id)], limit=1).inverse_company_rate
        if rate:
            new_price += self.cost_usd * rate
        else:
            new_price += self.cost_usd * 1
        self.standard_price = new_price
        for item in self.product_variant_ids:
            item.standard_price = new_price

    @api.depends('taxes_id', 'list_price_usd')
    def _compute_tax_string_usd(self):
        for record in self:
            record.tax_string_usd = record._construct_tax_string_usd(record.list_price_usd)
            
    def _construct_tax_string_usd(self, price):
        currency_usd_id = self.currency_usd_id
        res = self.taxes_id.compute_all(price, product=self, partner=self.env['res.partner'])
        joined = []
        included = res['total_included']
        if currency_usd_id.compare_amounts(included, price):
            joined.append(_('%s Incl. Taxes', format_amount(self.env, included, currency_usd_id)))
        excluded = res['total_excluded']
        if currency_usd_id.compare_amounts(excluded, price):
            joined.append(_('%s Excl. Taxes', format_amount(self.env, excluded, currency_usd_id)))
        if joined:
            tax_string_usd = f"(= {', '.join(joined)})"
        else:
            tax_string_usd = " "
        return tax_string_usd
            
            
    
class ProductProduct(models.Model):
    _inherit = "product.product"

    def _set_currency_usd_id(self):
        usd = self.env.ref("base.USD")
        return usd

    payment_method = fields.Selection(string="Forma de Pago", selection=[("Crédito", "Crédito"),
                                                                         ("Contado", "Contado")])
    quotation = fields.Char(string="Cotización")
    observation_note = fields.Text(string="Observación")
    measures_in_cm = fields.Char(string="Medidas en cm")
    raw_material = fields.Char(string="Materia Prima")
    mile_price_usd = fields.Float(string="Precio por Millar $", related='product_tmpl_id.mile_price_usd', digits=(12,2), store=False)
    mile_price = fields.Float(string="Precio por Millar Bs.", related='product_tmpl_id.mile_price', digits=(12,2), store=False)
    product_tmpl_id = fields.Many2one(comodel_name='product.template',
                                      string='Producto')
    currency_usd_id = fields.Many2one(comodel_name="res.currency",
                                      string="USD",
                                      default=_set_currency_usd_id)
    mile_standard_price_usd = fields.Float(string="Costo por Millar $",
                                           digits=(12,2),
                                           related='product_tmpl_id.mile_standard_price_usd')
    mile_standard_price_bs = fields.Float(string="Costo por Millar Bs.",
                                          digits=(12,2),
                                          related='product_tmpl_id.mile_standard_price_bs')
    tax_string_usd = fields.Char(compute='_compute_tax_string_usd')

    cost_usd = fields.Float(string="Coste $", related='product_tmpl_id.cost_usd')
            
    @api.depends('list_price_usd', 'product_tmpl_id', 'taxes_id')
    def _compute_tax_string(self):
        for record in self:
            record.tax_string = record.product_tmpl_id._construct_tax_string(record.list_price_usd)    