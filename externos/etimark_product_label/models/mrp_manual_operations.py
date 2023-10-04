# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MrpManualOperations(models.Model):

    _name = 'mrp.manual.operations'
    _description = """Manuales de Operaciones"""
    _rec_name = "manual_operations"

    manual_operations = fields.Text(string="Manual de Operaciones", 
                                    default="ACF-7.5.3-03 Rev 1 Edi. 1", 
                                    help="""Información del manual de operaciones de la fabricación del producto""",
                                    required=True)
    is_active = fields.Boolean(string="Activo?") 