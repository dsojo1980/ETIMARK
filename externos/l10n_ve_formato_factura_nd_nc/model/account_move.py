from odoo import _, api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'



    buys_name = fields.Char(string='Orden de Compra', readonly=True, copy=False)
    ref_orden_aux = fields.Char(compute='_compute_prueba', string='Orden de Compra')



    @api.depends('reason')
    def _compute_prueba(self):
        for move in self:
            valor = ''
            busca = self.env['account.move'].search([('name', '=', move.reason)])
            if busca:
                for det in busca:
                    valor = det.buys_name
                    break  # Si solo deseas el primer registro coincidente, puedes agregar un break aquí
            move.ref_orden_aux = valor


    
