from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    machine_speed = fields.Float('Velocidad de maquina')
    machine_reading = fields.Float('Lectura de maquina')
    number_coils = fields.Integer('Numero de bobinas P.A')
    waste_standard = fields.Float(string="Desperdicio Estándar")
    paper_width_inches_theoretical = fields.Float('Ancho de papel en pulgadas Teórico')
    paper_width_inches_actual = fields.Float('Ancho de papel en pulgadas Real')
    theoretical_length = fields.Float('Longitud del P.A (M) teórica')
    natural_process_waste = fields.Float('Desperdicio natural del proceso')
    show_report = fields.Boolean(string="Mostrar en Informe", default=False)
    total_waste_percentage = fields.Float(string="Total Waste Percentage")

    @api.onchange("waste_standard")
    def _get_total_waste_percentage(self):
        machine_count = 0
        machine = self.env['mrp.workcenter'].search([])
        for workcenter in machine:
            machine_count += len(workcenter)
        self.total_waste_percentage = machine_count
            # total_waste_standard = sum(workcenter.waste_standard) if isinstance(workcenter.waste_standard, list) else workcenter.waste_standard
            # machine_count = len(self)
            # if machine_count > 0:
            #     total_waste_percentage = total_waste_standard / machine_count
            # else:
            #     total_waste_percentage = 0.0
            # workcenter.total_waste_percentage = total_waste_percentage