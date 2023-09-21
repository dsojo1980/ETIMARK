# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MrpStorageConditions(models.Model):

    _name = 'mrp.storage.conditions'
    _description = """Condiciones de Almacenamiento"""
    _rec_name = "storage_conditions"

    storage_conditions = fields.Text(string="Condiciones de almacenamiento",
                                     help="""Información del almacenamiento del producto
                                     ,el cual debe ser constante en la impresión de todas
                                     las etiquetas.""",
                                     required=True)
    is_active = fields.Boolean(string="Activo?")