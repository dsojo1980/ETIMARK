from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    label_height_mm = fields.Float('Alto etiqueta mm')
    label_width_mm = fields.Float('Ancho etiqueta mm')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    label_height_mm = fields.Float('Alto etiqueta mm')
    label_width_mm = fields.Float('Ancho etiqueta mm')
