from odoo import _, api, fields, models
import random

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    nro_certificado=fields.Integer()


    def certificado(self):
        return self.env.ref('ext_certificado_calidad.action_certification_report').report_action(self)

    def formato_fecha(self,date):
        fecha = str(date)
        fecha_aux=fecha
        ano=fecha_aux[0:4]
        mes=fecha[5:7]
        dia=fecha[8:10]  
        resultado=dia+"/"+mes+"/"+ano
        return resultado

    def certificado_nro(self):
        if self.nro_certificado:
            nro=self.nro_certificado
        else:
            nro=random.randint(1, 10000)
            verifica=self.env['mrp.production'].search([('nro_certificado','=',nro)])
            if not verifica:
                self.nro_certificado=nro
            else:
                while verifica:
                    nro=random.randint(1, 10000)
                    verifica=self.env['mrp.production'].search([('nro_certificado','=',nro)])
        return nro

    def medidas(self):
        txt=str(self.product_id.label_width_mm)+'mm * '+str(self.product_id.label_height_mm)+'mm'
        return txt