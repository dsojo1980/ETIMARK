from odoo import models, fields, api


class ReportProductionIndicators(models.Model):
    _name = 'report.production.indicator'
    _description = 'Report Production Indicator'

    name = fields.Char(string="Name")
    create_date = fields.Date(string='create_date')
    ending_date = fields.Date(string='ending_date')
    mrp_production_id = fields.Many2one('mrp.production', string="Mrp Production", readonly=True)
    lot_number_id = fields.Many2one('stock.production.lot',string="Numero de lote", readonly=True)
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
    number_labels_produced = fields.Integer('Numero de etiquetas producidas (L.M)', readonly=True)
    number_labels_produced_coil = fields.Integer('Numero de etiquetas producidas por bobina', readonly=True)
    number_approved_labels = fields.Integer('Numero de etiquetas aprobadas', readonly=True)
    number_labels_rejected = fields.Integer('Numero de etiquetas rechazadas', readonly=True)
    square_meters = fields.Integer(string="Mt2 (Etiquetas Rechazadas)")
    # total_number_approved_labels = fields.Integer('Total de etiquetas aprobadas', readonly=True)
    waste_percentage = fields.Float('% de Desperdicio', readonly=True)
    machine_name_id = fields.Many2one('mrp.workcenter',string="Machine Name")
    cost = fields.Float(string="Costo")
