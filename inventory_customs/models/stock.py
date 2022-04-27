# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_log = logging.getLogger("___name: %s" % __name__)


class StockMoveTt(models.Model):
    _inherit = "stock.move"

    tt_with_moto = fields.Boolean(string="Traslado de motos", compute="_compute_with_moto", store=True)

    def _compute_with_moto(self):
        for reg in self:
            _log.info("Calculando categoría.")
            # Buscamos en la categoría de inventario
            if reg.product_id.product_inv_categ and reg.product_id.product_inv_categ in ["moto", "Moto"]:
                _log.info("\nEs una moto")
                reg.tt_with_moto = True

            # Marcamos como no encontrada.
            else:
                _log.info("\nNOOO Es una moto o no tiene categoría el producto.")
                reg.tt_with_moto = False


class StockMoveLineC(models.Model):
    _inherit = "stock.move.line"

    tt_motor_number = fields.Char(string="Número de motor")
    tt_color = fields.Char(string="Color")
    tt_inventory_number = fields.Char(string="Número de inventario")


class StockProductionLotTt(models.Model):
    _inherit = "stock.production.lot"

    tt_number_motor = fields.Char(string="Número de motor")
    tt_color = fields.Char(string="Color")
    tt_inventory_number = fields.Char(string="Número de inventario")