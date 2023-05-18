import base64
import xlwt
import io

from datetime import date, datetime  # , timedelta
from odoo import api, fields, models, _

ls_report =  [('PI', 'Production Indicator'),
              ('AS', 'Average Shrinkage')]

class WizardReportIndicator(models.TransientModel):
    _name = "wizard.report.indicator"

    create_date = fields.Date(string='create_date')
    ending_date = fields.Date(string="ending_date")
    company_id = fields.Many2one('res.company', string='Company',
        default=lambda self: self.env.company)
    report = fields.Selection(ls_report, string='Report Type') 

    def report_indicator(self):
        return self.env.ref("sale_to_manufacture.report_production_indicator_action").report_action(self)
    
    def report_production_indicator(self):
        if self.report == 'PI':
            lines = []
            indicator = self.env['report.production.indicator'].search([('create_date', '=', self.create_date),('ending_date', '=', self.ending_date)])
            for i in indicator:

                lines.append({
                    'lote': i.lot_number_id.name,
                    'Pedido': i.order_number,
                    'Etiqueta': i.label,
                    'Operador': i.operator,
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
                    'total_number_approved_labels': i.total_number_approved_labels,
                    'waste_percentage': i.waste_percentage,
                    })
            return lines

    def averag_shrinkage(self):
        if self.report == 'AS':
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Average Shrinkage', cell_overwrite_ok=True)

            head_style = xlwt.easyxf(
                "font: bold 1; align:horiz center; align:vert center; alignment: wrap True;"
                "borders: top dashed, bottom dashed, left dashed, right dashed; pattern: pattern solid;"
                "borders: top_color black, bottom_color black, right_color black, left_color black,")
            body_style = xlwt.easyxf(
                "font: bold 1; align:horiz center; align:vert center; alignment: wrap True;"
                "borders: top dashed, bottom dashed, left dashed, right dashed; pattern: pattern solid, fore_colour white;"
                "font: bold off, color black; borders: top_color black, bottom_color black, right_color black, left_color black,"
                "left thin, right thin, top thin, bottom thin; pattern: pattern solid, fore_color white;")

                # # where_clause = "1=1"
                # select = """
                # SELECT rule.name, rule.id, rule.code,
                # COALESCE(SUM(
                #     CASE
                #         WHEN category.code = 'DED' THEN line.total
                #     END)) as total_DED,
                # COALESCE(SUM(
                #     CASE
                #         WHEN category.code <> 'DED' THEN line.total
                #     END)) as total_ASIG ,
                # COUNT(distinct slip.employee_id) as emp
                # FROM hr_payslip_line AS line
                # INNER JOIN hr_payslip AS slip ON line.slip_id = slip.id
                # INNER JOIN hr_salary_rule rule ON line.salary_rule_id = rule.id
                # INNER JOIN hr_salary_rule_category category ON rule.category_id = category.id
                # INNER JOIN hr_payslip_run AS run ON run.id = slip.payslip_run_id
                # WHERE %s = run.id
                # GROUP BY rule.id, rule.name, rule.code
                # ORDER BY total_DED ASC
                # """

                # # select = select % (where_clause)
                # self.env.cr.execute(select, [payrun.id,])
                # results = self.env.cr.dictfetchall()

            ws.row(1).height = 800
            ws.col(1).width = 6000
            ws.col(2).width = 6000
            ws.col(3).width = 6000
            ws.col(4).width = 6000
            ws.col(5).width = 6000
            ws.col(6).width = 6000
            ws.col(7).width = 6000
            ws.col(8).width = 6000

            ws.write(1, 1, 'TOTAL ETIQUETAS', head_style)
            ws.write(1, 2, 'MT2 Etiquetas producidas;', head_style)
            ws.write(1, 3, 'TOTAL ETIQUETAS APROBADAS', head_style)
            ws.write(1, 4, 'MT2 Etiquetas Aprobadas', head_style)
            ws.write(1, 5, 'TOTAL ETIQUETAS RECHAZADAS', head_style)
            ws.write(1, 6, 'MT2 Etiquetas Rechazadas', head_style)
            ws.write(1, 7, 'Costo por MT2 en Bs.', head_style)
            ws.write(1, 8, 'Desperdicio Standard', head_style)
            ws.write(1, 9, '% DESP', head_style)

            workcenter_machine = []
            total = 0
            total_Mt2 = 0
            totalA = 0
            total_Mt2_t = 0
            totalR = 0
            total_waste = 0
            row = 2

            workcenter = self.env['mrp.workcenter'].search([])
            for w in workcenter:
                number_labels_produced_coil = 0
                Mt2_produced = 0
                total_number_approved_labels = 0
                Mt2_theoretical = 0
                number_labels_rejected = 0
                waste_percentage = 0

                average_shrinkage = self.env['report.production.indicator'].search([('create_date', '=', self.create_date),('ending_date', '=', self.ending_date)])
                for i in average_shrinkage:
                    if i.machine_name_id.id == w.id:
                        number_labels_produced_coil += i.number_labels_produced_coil
                        Mt2_produced += i.Mt2_produced
                        total_number_approved_labels += i.total_number_approved_labels
                        Mt2_theoretical += i.Mt2_theoretical
                        number_labels_rejected += i.number_labels_rejected
                        waste_percentage += i.waste_percentage

                workcenter_machine.append({
                    'machine_name': w.name,
                    'number_labels_produced_coil': number_labels_produced_coil,
                    'Mt2_produced': Mt2_produced,
                    'total_number_approved_labels': total_number_approved_labels,
                    'Mt2_theoretical': Mt2_theoretical,
                    'number_labels_rejected': number_labels_rejected,
                    'waste_percentage': waste_percentage,
                })

            for workcenter in workcenter_machine:
                total += workcenter['number_labels_produced_coil']
                total_Mt2 += workcenter['Mt2_produced']
                totalA += workcenter['total_number_approved_labels']
                total_Mt2_t += workcenter['Mt2_theoretical']
                totalR += workcenter['number_labels_rejected']
                total_waste += workcenter['waste_percentage']

                ws.write(row, 0, workcenter['machine_name'], head_style)
                ws.write(row, 1, workcenter['number_labels_produced_coil'], head_style)
                ws.write(row, 2, workcenter['Mt2_produced'], head_style)
                ws.write(row, 3, workcenter['total_number_approved_labels'], head_style)
                ws.write(row, 4, workcenter['Mt2_theoretical'], head_style)
                ws.write(row, 5, workcenter['number_labels_rejected'], head_style)
                ws.write(row, 6, '0.0', head_style)
                ws.write(row, 7, '0.0', head_style)
                ws.write(row, 8, '0.0', head_style)
                ws.write(row, 9, workcenter['waste_percentage'], head_style)
                ws.row(row).height = 800
                row += 1

            if totalA > 0 and totalR > 0 and total > 0:
                ws.write(row, 0, 'Total', head_style)
                ws.write(row, 1, total, head_style)
                ws.write(row, 2, total_Mt2, head_style)
                ws.write(row, 3, totalA, head_style)
                ws.write(row, 4, total_Mt2_t, head_style)
                ws.write(row, 5, totalR, head_style)
                ws.write(row, 6, '0.0', head_style)
                ws.write(row, 7, '0.0', head_style)
                ws.write(row, 8, '0.0', head_style)
                ws.write(row, 9, total_waste, head_style)

                ws.write(row + 1, 1, (total * 0.05), head_style)
                ws.write(row + 1, 3, (totalA * 0.05), head_style)
                ws.write(row + 1, 5, (totalR * 0.05), head_style)

                ws.write(row + 2, 3, round((totalA / total) * 100, 2), head_style)
                ws.write(row + 2, 5, round((totalR / total) * 100, 2), head_style)










        # for i in average_shrinkage:
        # average_shrinkage = self.env['report.production.indicator'].search([])
        # for i in average_shrinkage.mrp_production_id.workorder_ids:
            # ws.write(row, 0, i.machine_name_id.name, body_style)
        #     row += 1
        #     print('\n')
        #     print(i.workcenter_id.name)
                #     if i.get('total_asig'):
                #         total_asig += i.get('total_asig')
                #     if i.get('total_ded'):
                #         total_ded += i.get('total_ded')
                #     ws.write(row, 0, i['code'], body_style)
                #     ws.write(row, 1, i['name'], body_style)
                #     ws.write(row, 2, i['emp'], body_style)
                #     ws.write(row, 3, i['total_asig'], body_style)
                #     ws.write(row, 4, i['total_ded'], body_style)
                #     ws.row(row).height = 800
                #     row += 1
                # ws.write(row, 2, "Total", body_style)
                # ws.write(row + 1, 2, "Total a pagar", body_style)
                # ws.write(row + 1, 3, " ", body_style)
                # ws.write(row, 3, total_asig, body_style)
                # ws.write(row, 4, total_ded, body_style)
                # ws.write(row + 1, 4, (total_asig - total_ded), body_style)

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