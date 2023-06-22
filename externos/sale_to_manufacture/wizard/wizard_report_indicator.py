import base64
import xlwt
import io
import logging

from datetime import date, datetime  # , timedelta
from odoo import api, fields, models, _
_logger = logging.getLogger(__name__)

ls_report =  [('PI', 'Production Indicator'),
              ('AS', 'Average Shrinkage')]

class WizardReportIndicator(models.TransientModel):
    _name = "wizard.report.indicator"

    date_create = fields.Date(string='create_date', default=False)
    date_ending = fields.Date(string="ending_date")
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    report = fields.Selection(ls_report, string='Report Type') 

    def report_indicator(self):
        return self.env.ref("sale_to_manufacture.report_production_indicator_action").report_action(self)
    
    def report_production_indicator(self):
        if self.report == 'PI':
            lines = []
            indicator = self.env['report.production.indicator'].search([('create_date','>=',self.date_create),('create_date','<=',self.date_ending)])
            for i in indicator:
                lines.append({
                    'lote': i.lot_number_id.name,
                    'Pedido': i.order_number,
                    'Etiqueta': i.label,
                    'operator': i.operator,
                    'machine_speed': i.machine_speed,
                    'machine_reading': i.machine_reading,
                    'label_height_mm': i.label_height_mm,
                    'label_width_mm': i.label_width_mm,
                    'number_coils': i.number_coils,
                    'paper_width_inches_theoretical': i.paper_width_inches_theoretical,
                    'paper_width_inches_actual': i.paper_width_inches_actual,
                    'theoretical_length': i.theoretical_length,
                    'natural_process_waste': i.natural_process_waste,
                    'length_PA_real': i.length_PA_real,
                    'number_labels_per_reel': i.number_labels_per_reel,
                    'Mt2_theoretical': i.Mt2_theoretical,
                    'Mt2_produced': i.Mt2_produced,
                    'number_labels_produced': i.number_labels_produced,
                    'number_labels_produced_coil': i.number_labels_produced_coil,
                    'number_approved_labels': i.number_approved_labels,
                    'number_labels_rejected': i.number_labels_rejected,
                    # 'total_number_approved_labels': i.total_number_approved_labels,
                    'waste_percentage': i.waste_percentage,
                    })
            return lines

    def averag_shrinkage(self):
        if self.report == 'AS':
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Average Shrinkage', cell_overwrite_ok=True)

            body_style = xlwt.easyxf(
                "font: bold 1; align:horiz center; align:vert center; alignment: wrap True;"
                "borders: top dashed, bottom dashed, left dashed, right dashed; pattern: pattern solid, fore_colour white;"
                "font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black,"
                "left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;")

            ws.row(1).height = 800
            ws.col(1).width = 6000
            ws.col(2).width = 6000
            ws.col(3).width = 6000
            ws.col(4).width = 6000
            ws.col(5).width = 6000
            ws.col(6).width = 6000
            ws.col(7).width = 6000
            ws.col(8).width = 6000

            ws.write(1, 1, 'TOTAL ETIQUETAS', body_style)
            ws.write(1, 2, 'MT2 Etiquetas producidas;', body_style)
            ws.write(1, 3, 'TOTAL ETIQUETAS APROBADAS', body_style)
            ws.write(1, 4, 'MT2 Etiquetas Aprobadas', body_style)
            ws.write(1, 5, 'TOTAL ETIQUETAS RECHAZADAS', body_style)
            ws.write(1, 6, 'MT2 Etiquetas Rechazadas', body_style)
            ws.write(1, 7, 'Costo por MT2 en $.', body_style)
            ws.write(1, 8, 'Desperdicio Standard', body_style)
            ws.write(1, 9, '% DESP', body_style)

            machine_name = ''
            number_labels_produced_coil = 0
            Mt2_produced = 0
            total_number_approved_labels = 0
            Mt2_theoretical = 0
            number_labels_rejected = 0
            waste_percentage = 0
            square_meters = 0
            cost = 0
            waste_standard = 0
            desp = 0
            row = 2

            workcenter = self.env['mrp.workcenter'].search([])
            for w in workcenter:
                if w.show_report == True:
                    average_shrinkage = self.env['report.production.indicator'].search([('create_date','>=',self.date_create),('create_date','<=',self.date_ending)])
                    for i in average_shrinkage:
                        if i.machine_name_id.id == w.id:

                            machine_name = w.name,
                            number_labels_produced_coil += i.number_labels_produced_coil
                            Mt2_produced += i.Mt2_produced
                            total_number_approved_labels += i.number_approved_labels
                            Mt2_theoretical += (Mt2_produced * total_number_approved_labels) / number_labels_produced_coil
                            number_labels_rejected += i.number_labels_rejected
                            square_meters += i.square_meters
                            waste_percentage += i.waste_percentage
                            cost = i.cost
                            waste_standard += w.waste_standard
                            desp = (number_labels_rejected / number_labels_produced_coil) * 100

                            ws.write(row, 0, machine_name, body_style)
                            ws.write(row, 1, format(number_labels_produced_coil, '.2f'), body_style)
                            ws.write(row, 2, format(Mt2_produced, '.2f'), body_style)
                            ws.write(row, 3, format(total_number_approved_labels, '.2f'), body_style)
                            ws.write(row, 4, format(Mt2_theoretical, '.2f'), body_style)
                            ws.write(row, 5, format(number_labels_rejected, '.2f'), body_style)
                            ws.write(row, 6, format(square_meters, '.2f'), body_style)
                            ws.write(row, 7, format(cost, '.2f'), body_style)
                            ws.write(row, 8, format(waste_standard, '.2f'), body_style)
                            ws.write(row, 9, format(desp, '.2f'), body_style)
                            ws.row(row).height = 800
                            row += 1

            total_number_labels_produced_coil = 0
            total_Mt2_produced = 0
            total_total_number_approved_labels = 0
            total_number_labels_rejected = 0
            total_waste_percentage = 0
            total_waste_standard = 0
            total_square_meters = 0
            total_cost = 0
            total_Mt2_theoretical = 0
            total_waste = 0
            total_number_labels_produced_coil += number_labels_produced_coil
            total_Mt2_produced += Mt2_produced
            total_total_number_approved_labels += total_number_approved_labels
            total_number_labels_rejected += number_labels_rejected
            total_waste_percentage += waste_percentage
            total_waste_standard += waste_standard
            total_square_meters += square_meters
            total_cost += cost
            total_Mt2_theoretical += Mt2_theoretical
            total_waste += desp

            ws.write(row, 0, 'Total', body_style)
            ws.write(row, 1, format(total_number_labels_produced_coil,'.2f'), body_style)
            ws.write(row, 2, format(total_Mt2_produced,'.2f'), body_style)
            ws.write(row, 3, format(total_total_number_approved_labels,'.2f'), body_style)
            ws.write(row, 4, format(total_Mt2_theoretical,'.2f'), body_style)
            ws.write(row, 5, format(total_number_labels_rejected,'.2f'), body_style)
            ws.write(row, 6, format(total_square_meters,'.2f'), body_style)
            ws.write(row, 7, format(total_cost,'.2f'), body_style)
            ws.write(row, 8, format(total_waste_standard,'.2f'), body_style)
            ws.write(row, 9, format(total_waste / (row - 2),'.2f'), body_style)

            ws.write(row + 1, 1, format((total_number_labels_produced_coil * 0.05),'.2f'), body_style)
            ws.write(row + 1, 3, format((total_total_number_approved_labels * 0.05),'.2f'), body_style)
            ws.write(row + 1, 5, format((total_number_labels_rejected * 0.05),'.2f'), body_style)

            ws.write(row + 2, 3, format((total_number_approved_labels / number_labels_produced_coil) * 100, '.2f'), body_style)
            ws.write(row + 2, 5, format((number_labels_rejected / number_labels_produced_coil) * 100, '.2f'), body_style)
            wb.save('/tmp/average_shrinkage.xls')
            file = open('/tmp/average_shrinkage.xls', 'rb')
            out = file.read()
            attach_vals = {'name': 'average_shrinkage.xls',
                            'datas': base64.b64encode(out),
                            'res_model': 'wizard.report.indicator',
                            'public': True,
                            'mimetype': 'text/plain',
                            'store_fname': 'average_shrinkage.xls'}
            doc_id = self.env['ir.attachment'].create(attach_vals)
            return {
                'name': 'Average Shrinkage',
                'type': 'ir.actions.act_url',
                'url': 'web/content/%d?download=true' % doc_id.id,
                'target': 'self',
            }