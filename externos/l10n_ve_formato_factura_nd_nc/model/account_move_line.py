# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.exceptions import Warning
from odoo.tools.misc import formatLang, format_date, get_lang
from datetime import datetime, timedelta



class AccountMove(models.Model):
    _inherit = 'account.move.line'

    mile_price_usd = fields.Float(string="Precio por Milla $", 
                                  digits=(12,2),
                                  compute='_mile_price_usd',
                                  store=False)

    mile_price = fields.Float(string="Precio por Milla Bs.", 
                                  digits=(12,2),
                                 compute='_mile_price_bs',
                                store=False)

    price_unit_rate = fields.Float(digits=(12,4))
    price_unit = fields.Float(digits=(12,4))
    
    @api.onchange('discount')
    def _mile_price_usd(self):
      for record in self:
        if self.move_id.os_currency_rate==0:
          tasa=1
        else:
          tasa=self.move_id.os_currency_rate
        price = record.price_unit_rate if self.company_id.currency_id.id==self.move_id.currency_id.id else record.price_unit_rate/tasa
        #price = record.price_unit_rate
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
        price = record.price_unit if self.company_id.currency_id.id==self.move_id.currency_id.id else record.price_unit*self.move_id.os_currency_rate
        #price = record.price_unit
        dis = record.discount
        if dis == 0:
          total = price * 1000
          record.mile_price = total
        if dis > 0:
          price_mil = price * 1000
          discount = price_mil * (dis / 100)
          total = price_mil - discount
          record.mile_price = total
   
   


