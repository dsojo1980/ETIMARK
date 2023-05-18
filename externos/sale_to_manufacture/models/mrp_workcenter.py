from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    machine_speed = fields.Float('Velocidad de maquina')
    machine_reading = fields.Float('Lectura de maquina')
    label_height_mm = fields.Float('Alto etiqueta mm')
    label_width_mm = fields.Float('Ancho etiqueta mm')
    number_coils = fields.Integer('Numero de bobinas P.A')
    paper_width_inches_theoretical = fields.Float('Ancho de papel en pulgadas Teórico')
    paper_width_inches_actual = fields.Float('Ancho de papel en pulgadas Real')
    theoretical_length = fields.Float('Longitud del P.A (M) teórica')
    natural_process_waste = fields.Float('Desperdicio natural del proceso')