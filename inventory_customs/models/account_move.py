# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_log = logging.getLogger("___name: %s" % __name__)


class AccountMoveItt(models.Model):
    _inherit = "account.move"

    def _get_invoiced_lot_values_tt(self, product_id=None):
        # Poner aquí la restricción de la compañia.
        if self.move_type != "out_invoice" or self.state == 'draft':
            return False
        sale_lines = self.invoice_line_ids.sale_line_ids
        # Filter lines for specific product
        stock_move_lines = sale_lines.move_ids.filtered(lambda r: r.state == 'done').move_line_ids.filtered(lambda r: r.product_id.id == product_id.id)
        data = []
        for line in stock_move_lines:
            if not line.product_id.product_inv_categ or not line.product_id.product_inv_categ in ["moto", "Moto"]:
                continue
            # Put: color; inv num,
            data.append({
                'serial': line.lot_id.name,
                'motor_num': line.lot_id.tt_number_motor,
                'color': line.lot_id.tt_color,
                'inv_num': line.lot_id.tt_inventory_number,
                'brand': line.product_id.brand_id.name,
                'model': line.product_id.moto_model,
                'moto_cil': line.product_id.moto_cilindros,
                'moto_desp': line.product_id.moto_despl
            })

        if len(data) > 0:
            return data
        # Si no se origina en sale.order, entonces pos.order:..
        if not self.pos_order_ids:
            return False
        pols = self.pos_order_ids.mapped('lines').mapped('pack_lot_ids').filtered(lambda x: x.product_id.id == product_id.id)
        for pol in pols:
            lot_domain = [
                ('name', '=like', pol.lot_name),
                ('product_id', '=', pol.product_id.id),
                ('company_id', '=', pol.company_id.id)
            ]
            ori_lot = self.env['stock.production.lot'].search(lot_domain)
            if not ori_lot:
                continue
            data.append({
                'serial': ori_lot.name,
                'motor_num': ori_lot.tt_number_motor,
                'color': ori_lot.tt_color,
                'inv_num': ori_lot.tt_inventory_number,
                'brand': ori_lot.product_id.brand_id.name,
                'model': ori_lot.product_id.moto_model,
                'moto_cil': ori_lot.product_id.moto_cilindros,
                'moto_desp': ori_lot.product_id.moto_despl
            })

        if len(data) > 0:
            return data
        return False

    def _set_num_pedimento(self):
        if self.move_type != "out_invoice" or self.state == 'draft':
            return False
        sale_lines = self.invoice_line_ids.sale_line_ids
        # Filter lines for specific product
        stock_move = sale_lines.move_ids.filtered(lambda r: r.state == 'done').move_line_ids.filtered(lambda r: r.product_id.id == product_id.id)
        data = []