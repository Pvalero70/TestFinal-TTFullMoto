# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError, Warning
#import xml.etree.ElementTree as etree
from lxml import etree

_logger = logging.getLogger(__name__)


class ResUserInheritDiscount(models.Model):
    _inherit = 'product.category'

    account_credit_note_id = fields.Many2one('account.account',"Cuenta de nota de credito")
    account_discount_id = fields.Many2one('account.account', "Cuenta de descuento o bonificacion")



class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountMoveInherit, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                  toolbar=toolbar, submenu=submenu)

        context = self.env.context
        _logger.info("ACCOUNT MOVE MODEL:: view type %s, permiso factura client %s, context default_move_type %s",view_type, self.env.user.has_group('credit_note_restrict.factura_client_group'),context.get('default_move_type'))
        doc = etree.XML(res['arch'])


        if view_type in ['form','tree']:
            if (not self.env.user.has_group('credit_note_restrict.factura_client_group')) and context.get('default_move_type') == 'out_invoice': #Facturas de clientes
                for node_form in doc.xpath("//form"):
                    node_form.set("create", 'false')
                for node_form in doc.xpath("//tree"):
                    node_form.set("create", 'false')

            if (not self.env.user.has_group('credit_note_restrict.credit_note_client_group')) and context.get('default_move_type') == 'out_refund': #Notas de credito en clientes
                for node_form in doc.xpath("//form"):
                    node_form.set("create", 'false')
                for node_form in doc.xpath("//tree"):
                    node_form.set("create", 'false')

            if (not self.env.user.has_group('credit_note_restrict.factura_proveedor_group')) and context.get('default_move_type') == 'in_invoice': #Facturas en proveedores
                for node_form in doc.xpath("//form"):
                    node_form.set("create", 'false')
                for node_form in doc.xpath("//tree"):
                    node_form.set("create", 'false')

            if (not self.env.user.has_group('credit_note_restrict.reembolso_proveedor_group')) and context.get('default_move_type') == 'in_refund': #reembolsos en proveedores
                for node_form in doc.xpath("//form"):
                    node_form.set("create", 'false')
                for node_form in doc.xpath("//tree"):
                    node_form.set("create", 'false')
        res['arch'] = etree.tostring(doc)
        return res


class AccountTranzientReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    reason_select = fields.Selection([ ('devolucion', 'Devolucion'),('descuento', 'Descuento o Bonificacion'),('otro', 'Otro')],'Type', default='devolucion')

    def reverse_moves(self):
        _logger.info('REVERSE_MOVES:: en mi funcion')

        res = super(AccountTranzientReversal, self).reverse_moves()
        return res
