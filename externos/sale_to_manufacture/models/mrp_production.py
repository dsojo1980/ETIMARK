from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    machine_number = fields.Char(string='Número de maquina')
    tag_number = fields.Float(string='Número de etiqueta')
    number_order = fields.Char(string='Numero de orden')
    client_number = fields.Char(string='Cliente / Numero de cliente')
    operator = fields.Char(string="Operador")

    label_height_mm = fields.Float(related="product_id.label_height_mm", string="Alto etiqueta mm")
    label_width_mm = fields.Float(related="product_id.label_width_mm", string='Ancho etiqueta mm')
    length_PA_Real = fields.Float(string='Longitud del P.A (M) Real', readonly=True)
    number_labels_per_reel = fields.Float(string='Numero de etiquetas por bobina')
    Mt2_theoretical = fields.Float(string='Mt2(metros cuadrados) teóricos', readonly=True)
    Mt2_produced = fields.Float(string='Mt2(metros cuadrados) Producidos', readonly=True)
    number_labels_produced = fields.Float(string='Numero de etiquetas producidas L.M (Referencial)')
    number_labels_produced_coil = fields.Float(string='Numero de etiquetas producidas por bobina', readonly=True)
    number_approved_labels = fields.Float(string='Numero de etiquetas aprobadas')
    number_labels_rejected = fields.Float(string='Numero de etiquetas rechazadas', readonly=True)
    square_meters = fields.Float(string="Mt2 (Etiquetas Rechazadas)")
    cost = fields.Float(string="Costo $", compute="_compute_cost_components")
    total_number_approved_labels = fields.Float('Total de etiquetas aprobadas')
    waste_percentage = fields.Float(string='% de Desperdicio', readonly=True)
    report_production_indicator_ids = fields.One2many('report.production.indicator', 'mrp_production_id' ,string="Report Production Indicator")

    def button_mark_done(self):
        res = super().button_mark_done()
        if self.state == 'done':
            self.state_update_production_indicators()
            self.onchange_shrinkage_process()
            print('\n')
        return res
    
    @api.depends("move_raw_ids")
    def _compute_cost_components(self):
        costs = 0
        for cost in self.move_raw_ids.product_id:
            costs += cost.cost_usd
        self.cost = costs
    
    def onchange_shrinkage_process(self):
        for i in self.workorder_ids:
            self.machine_number = i.workcenter_id.equipment_ids.machine_number
            # if self.length_PA_Real - i.workcenter_id.natural_process_waste < 1:
            #     pass
            # else:
            self.length_PA_Real = format((i.workcenter_id.theoretical_length - i.workcenter_id.natural_process_waste),'.4f')
            self.Mt2_theoretical = ((i.workcenter_id.paper_width_inches_theoretical * i.workcenter_id.number_coils * i.workcenter_id.theoretical_length) / 39.37)
            self.Mt2_produced = format(((i.workcenter_id.paper_width_inches_actual * i.workcenter_id.number_coils * i.workcenter_id.theoretical_length) / 39.37),'.4f')
            if self.product_id.label_height_mm > 0 or self.product_id.label_width_mm > 0:
                self.number_labels_produced_coil = ((self.Mt2_produced * 1000000) / (self.product_id.label_height_mm * self.product_id.label_width_mm))
            self.number_labels_rejected = self.number_labels_produced_coil - self.number_approved_labels
            if self.number_labels_produced_coil:
                self.square_meters = format((self.Mt2_produced * self.number_labels_rejected) / self.number_labels_produced_coil, '.4f')
            if self.number_labels_rejected > 0 or self.number_labels_produced_coil > 0:
                self.waste_percentage = ((self.number_labels_rejected ) / self.number_labels_produced_coil) * 100
                _logger.info(self.square_meters)
                _logger.info(self.number_labels_produced_coil)
                _logger.info(self.number_labels_rejected)
            _logger.info("Valor actualizado de square_meters: %s" % self.square_meters)
        # for components in self.move_raw_ids:  


    def state_update_production_indicators(self):
        list_value = []
        list_value_2 = []
        for i in self.workorder_ids:
            list_value.append((0, 0, {
                'name': self.name,
                'lot_number_id': self.lot_producing_id.id,
                'order_number': self.number_order,
                'label': self.product_id.name,
                'operator': self.operator,
                'machine_speed': i.workcenter_id.machine_speed,
                'machine_reading': i.workcenter_id.machine_reading,
                'label_height_mm': self.product_id.label_height_mm,
                'label_width_mm': self.product_id.label_width_mm,
                'number_coils': i.workcenter_id.number_coils,
                'paper_width_inches_theoretical': i.workcenter_id.paper_width_inches_theoretical,
                'paper_width_inches_actual': i.workcenter_id.paper_width_inches_actual,
                'theoretical_length': i.workcenter_id.theoretical_length,
                'natural_process_waste': i.workcenter_id.natural_process_waste,
                'length_PA_real': self.length_PA_Real,
                'number_labels_per_reel': self.number_labels_per_reel,
                'Mt2_theoretical': self.Mt2_theoretical,
                'Mt2_produced': self.Mt2_produced,
                'number_labels_produced': self.number_labels_produced,
                'number_labels_produced_coil': self.number_labels_produced_coil,
                'number_approved_labels': self.number_approved_labels,
                'number_labels_rejected': self.number_labels_rejected,
                'total_number_approved_labels': self.total_number_approved_labels,
                'waste_percentage': self.waste_percentage,
                'create_date': self.date_start,
                'ending_date': self.date_finished,
                'machine_name_id': i.workcenter_id.id,
                'square_meters': self.square_meters,
                'cost': self.cost,
            }))
        list_value_2.append(list_value[-1])
        self.update({'report_production_indicator_ids':list_value_2})
