# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
import logging


_logger = logging.getLogger(__name__)

class ResUserInheritDiscount(models.Model):
    _inherit = 'res.users'

    discount_ids = fields.One2many('res.users.discount','seller_id',String="Lista de Descuentos")


class ResUsersDiscount(models.Model):
    _name = 'res.users.discount'

    _description = "Model that saves discounts on product categories"

    seller_id = fields.Many2one('res.users' , 'Vendedor',)
    discount_permitted = fields.Integer('Descuento permitido')
    category_ids = fields.Many2many(comodel_name='product.category' , string='Categorias')


    def write(self, values):
        _logger.debug('Create a %s with vals %s', self._name, values)
        res = self.env.user.has_group('pos_user_restrict.user_discount_agente_group')
        grupos = self.env.user.groups_id
        _logger.info('resultado de grupo : %s : y grupos : %s', res, grupos)
        return super(ResUsersDiscount, self).write(values)

    @api.model_create_multi
    def create(self, vals):
        _logger.debug('Create a %s with vals %s', self._name, vals)
        res = self.env.user.has_group('pos_user_restrict.user_discount_agente_group')
        grupos = self.env.user.groups_id

        _logger.info('resultado de grupo : %s : y grupos : %s', res, grupos)
        return super(ResUsersDiscount, self).create(vals)
