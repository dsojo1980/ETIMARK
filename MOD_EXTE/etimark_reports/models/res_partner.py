# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _


class Partner(models.Model):
    _inherit = 'res.partner'
    
    nit_ve = fields.Char(string='Número de Identificación Tributaria',
                         help='Número de Identificación Tributaria')