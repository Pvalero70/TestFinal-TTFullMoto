# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError, Warning
from lxml import etree

_log = logging.getLogger("___name: %s" % __name__)

from lxml import etree


class PosOrderC(models.Model):
    _inherit = "product.template"

    # edit_price_sale = fields.Boolean("Editar precio de venta", compute='_compute_group_edit_sale_price', store=False)


    @api.onchange("list_price")
    def _onchangeprice(self):
        _log.info("Es numero %s,number %s",str(self.id).isnumeric(),self.id)
        if not str(self.id).isnumeric():
            return

        if self.env.user.has_group('product_price_restrict.product_sale_price_group') == False:
            raise ValidationError(_("Advertencia, no puedes modificar el precio de venta"))

    @api.onchange("standard_price")
    def _onchangestandarprice(self):
        if not str(self.id).isnumeric():
            return
        if self.env.user.has_group('product_price_restrict.product_price_group') == False:
            raise ValidationError(_("Advertencia, no puedes modificar el coste"))


