from odoo import models, fields, api


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    machine_number = fields.Char('Número de Maquina')

