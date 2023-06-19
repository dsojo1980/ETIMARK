from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    number_order = fields.Char('Numero de orden')
    client_number = fields.Char(related='partner_id.client_number', string='Cliente / Numero de cliente')

    def action_confirm(self):
        res = super().action_confirm()
        self.send_data_manufacturing()
        return res

    def send_data_manufacturing(self):
        list_value = []
        if self.client_number:
            for i in self.procurement_group_id.stock_move_ids.created_production_id.procurement_group_id.mrp_production_ids:
                i.write({'number_order': self.number_order,
                        'client_number': self.partner_id.name + ' / ' + self.client_number,
                        'user_id': self.user_id,
                        })
        else:
            raise ValidationError(_("El Número del cliente no esta registrado"))
