from odoo import models, fields, api


class ReportProductionIndicators(models.Model):
    _name = 'report.production.indicator'
    _description = 'Report Production Indicator'

    name_id = fields.Many2one("mrp.production",string="Name")
    create_date = fields.Date(string='create_date', readonly=True)
    ending_date = fields.Date(related='name_id.date_finished', readonly=True)
    mrp_production_id = fields.Many2one('mrp.production', string="Mrp Production", readonly=True)
    lot_number = fields.Char(related='name_id.lot_producing_id.name',string="Numero de lote", readonly=True)
    order_number = fields.Char(string="Numero de pedido", readonly=True)
    label = fields.Char(string="Etiqueta", readonly=True)
    operator = fields.Char(string="Operador", readonly=True)
    machine_speed = fields.Char(string="Velocidad de maquina", readonly=True)
    machine_reading = fields.Char(string="Lectura de maquina", readonly=True)
    label_height_mm = fields.Char(string="Alto etiqueta mm", readonly=True)
    label_width_mm = fields.Char(string="Ancho etiqueta mm", readonly=True)
    number_coils = fields.Char(string="Numero de bobinas P.A", readonly=True)
    paper_width_inches_theoretical = fields.Char(string="Ancho de papel en pulgadas Teórico", readonly=True)
    paper_width_inches_actual = fields.Char(string="Ancho de papel en pulgadas Real", readonly=True)
    theoretical_length = fields.Char(string="Longitud del P.A (M) teórica", readonly=True)
    natural_process_waste = fields.Char(string="Desperdicio natural del proceso", readonly=True)
    length_PA_real = fields.Char(string="Longitud del P.A (M) Real", readonly=True)
    number_labels_per_reel = fields.Char(string="Numero de etiquetas por bobina", readonly=True)
    Mt2_theoretical = fields.Float('Mt2(metros cuadrados) teóricos', readonly=True)
    Mt2_produced = fields.Float('Mt2(metros cuadrados) Producidos', readonly=True)
    number_labels_produced = fields.Float('Numero de etiquetas producidas (L.M)', readonly=True)
    number_labels_produced_coil = fields.Integer('Numero de etiquetas producidas por bobina', readonly=True)
    number_approved_labels = fields.Float('Numero de etiquetas aprobadas', readonly=True)
    number_labels_rejected = fields.Float('Numero de etiquetas rechazadas', readonly=True)
    square_meters = fields.Float(string="Mt2 (Etiquetas Rechazadas)", readonly=True)
    # total_number_approved_labels = fields.Float('Total de etiquetas aprobadas', readonly=True)
    waste_percentage = fields.Float('% de Desperdicio', readonly=True)
    machine_name_id = fields.Many2one('mrp.workcenter',string="Machine Name", readonly=True)
    cost = fields.Float(string="Costo", readonly=True)

    @api.onchange("waste_standard")
    def _get_total_waste_percentage(self):
        machine_count = 0
        machine = self.env['mrp.workcenter'].search([("show_report", "=", True)])
        for workcenter in machine:
            machine_count += len(workcenter)
        self.total_waste_percentage = machine_count
