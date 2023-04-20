# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    payment_method = fields.Selection(string='Forma de Pago', selection=[('Crédito', 'Crédito'),
                                                                         ('Contado', 'Contado')])
    elaborated = fields.Many2one(comodel_name='res.users', 
                                 string='Elaborado')
    reviewed = fields.Many2one(comodel_name='res.users',
                               string='Revisado')
    approved = fields.Many2one(comodel_name='res.users',
                               string='Aprobado')
    quotation = fields.Char(string='Cotización')
    observation_note = fields.Text(string='Observación')