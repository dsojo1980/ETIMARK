# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class ResCompany(models.Model):
    _inherit = 'res.company'

    account_payable_aux_id = fields.Many2one('account.account',company_dependent=True)
    account_receivable_aux_id = fields.Many2one('account.account',company_dependent=True)

    property_account_payable_vat_id = fields.Many2one('account.account',company_dependent=True)
    property_account_receivable_vat_id = fields.Many2one('account.account',company_dependent=True)
    retention_iva_rate = fields.Float()

    #account_anti_payable_aux_id = fields.Many2one('account.account',company_dependent=True)
    #account_anti_receivable_aux_id = fields.Many2one('account.account',company_dependent=True)