from odoo import models, fields, api


class Partners(models.Model):
    _inherit = 'res.partner'

    client_number = fields.Char('Cliente / Numero de cliente')
