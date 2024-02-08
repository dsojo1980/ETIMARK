from odoo import _, api, fields, models
import random
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    nro_certificado=fields.Char()


    def certificado(self):
        self.valida()
        return self.env.ref('ext_certificado_calidad.action_certification_report').report_action(self)

    def formato_fecha(self,date):
        fecha = str(date)
        fecha_aux=fecha
        ano=fecha_aux[0:4]
        mes=fecha[5:7]
        dia=fecha[8:10]  
        resultado=dia+"/"+mes+"/"+ano
        return resultado

    def certificado_nro_aleatorio(self):
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

    def valida(self):
        ban_papel=0
        busca=self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id)])
        if busca:
            for det in busca:
                if det.bom_line_ids:
                    for line in det.bom_line_ids:
                        if line.product_id.categ_id.tipo_producto=='papel':
                            ban_papel=ban_papel+1
                            if not line.product_id.espesor or not line.product_id.gramaje or not line.product_id.adhesivo:
                                raise UserError(_('Falta los datos como Gramaje, espesor o adhesivos. Favor incluir estos datos en la conf de la materia prima papel'))
            if ban_papel==0:
                raise UserError(_('En la receta no contiene como base papel. Por Favor incluir uno para poder imprimir el certificado. En Caso de que este, revise que la categoria del producto tenga como tipo Papel'))



    def certificado_nro(self):
        if self.nro_certificado:
            name=self.nro_certificado
        else:
            self.ensure_one()
            SEQUENCE_CODE = 'l10n_ve_certificado_calidad'
            company_id = self.env.company.id
            IrSequence = self.env['ir.sequence'].with_context(force_company=company_id)
            name = IrSequence.next_by_code(SEQUENCE_CODE)
            # si aún no existe una secuencia para esta empresa, cree una
            if not name:
                IrSequence.sudo().create({
                    'prefix': '00-',
                    'name': 'Secuencia certificado de calidad %s' % company_id,
                    'code': SEQUENCE_CODE,
                    'implementation': 'no_gap',
                    'padding': 5,
                    'number_increment': 1,
                    'company_id': company_id,
                })
                name = IrSequence.next_by_code(SEQUENCE_CODE)
            self.nro_certificado=name
        return name

    def medidas(self):
        txt=str(self.product_id.label_width_mm)+'mm * '+str(self.product_id.label_height_mm)+'mm'
        return txt

    def colores(self):
        cant=0
        busca=self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id)])
        #raise UserError(_('busca=%s')%busca)
        if busca:
            for det in busca:
                if det.bom_line_ids:
                    for line in det.bom_line_ids:
                        if line.product_id.categ_id.tipo_producto=='tinta':
                            cant=cant+1
        return cant

    def pantones(self):
        text=''
        busca=self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id)])
        if busca:
            for det in busca:
                if det.bom_line_ids:
                    for line in det.bom_line_ids:
                        if line.product_id.categ_id.tipo_producto=='tinta':
                            text=text+line.product_id.name+' / '
        return text

    def papel(self):
        text=''
        busca=self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id)])
        if busca:
            for det in busca:
                if det.bom_line_ids:
                    for line in det.bom_line_ids:
                        if line.product_id.categ_id.tipo_producto=='papel':
                            text=text+line.product_id.name+' / '
        return text

    def espesor(self):
        txt=''
        busca=self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id)])
        if busca:
            for det in busca:
                if det.bom_line_ids:
                    for line in det.bom_line_ids:
                        if line.product_id.categ_id.tipo_producto=='papel':
                            txt=line.product_id.espesor
        return txt

    def gramaje(self):
        txt=''
        busca=self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id)])
        if busca:
            for det in busca:
                if det.bom_line_ids:
                    for line in det.bom_line_ids:
                        if line.product_id.categ_id.tipo_producto=='papel':
                            txt=line.product_id.gramaje
        return txt

    def adhesivo(self):
        txt=''
        busca=self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_id.product_tmpl_id.id)])
        if busca:
            for det in busca:
                if det.bom_line_ids:
                    for line in det.bom_line_ids:
                        if line.product_id.categ_id.tipo_producto=='papel':
                            txt=line.product_id.adhesivo
        return txt
