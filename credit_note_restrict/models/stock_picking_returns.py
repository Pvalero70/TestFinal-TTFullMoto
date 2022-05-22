# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError, Warning
from lxml import etree

### notas de credito en contabilidad
_logger = logging.getLogger(__name__)


class StockPickingReturn(models.Model):
    _inherit = 'stock.picking'

    permiso_devolucion = fields.Boolean(string="Permiso devolucion", compute="_compute_devolucion_permiso", store=False)
    es_devolucion = fields.Boolean(string="Permiso devolucion", compute="_compute_es_devolucion", store=False)
    is_sent_mail = fields.Boolean(string="El correo ha sido enviado para aprobacion?",default=False)

    @api.onchange('picking_type_id')
    def _compute_devolucion_permiso(self):
        grupo_devolucion = self.env.user.has_group('credit_note_restrict.aprobe_devolucion_group')
        grupo_recepcion = self.env.user.has_group('credit_note_restrict.aprobe_devolucion_compra_group')
        if self.picking_type_id and (self.picking_type_id.sequence_code == 'DEV' or self.picking_type_id.name =='Devoluciones'):
            if grupo_devolucion:
                self.permiso_devolucion = True
            else:
                self.permiso_devolucion = False
        elif self.picking_type_id and (self.picking_type_id.sequence_code =='IN' or self.picking_type_id.name == 'Recepciones'):
            if grupo_recepcion:
                self.permiso_devolucion=True
            else:
                self.permiso_devolucion = False
        else:
            self.permiso_devolucion = True
        _logger.info("STOCK.PICKING::Computamos permiso dev %s",self.permiso_devolucion)

    @api.onchange('picking_type_id')
    def _compute_es_devolucion(self):
        if self.picking_type_id and (self.picking_type_id.sequence_code == 'DEV' or self.picking_type_id.name =='Devoluciones'):
            self.es_devolucion = True
        else:
            self.es_devolucion = False

    def button_solicitar_devolucion(self):
        gerente_encontrado = False
        if self.picking_type_id and self.picking_type_id.warehouse_id:
            almacen = self.picking_type_id.warehouse_id
            list_usuarios = self.env['res.users'].search([('property_warehouse_id', '=', almacen.id)])
            for usuario in list_usuarios:
                if usuario.has_group('credit_note_restrict.aprobe_devolucion_group'):
                    gerente_encontrado=True
                    body = "Hola.<br>"
                    body+= "En la compañía: "+str(self.company_id.name)+"<br>"
                    body += "Tienes el documento "+str(self.name)+" pendiente de aprobar, generado por una devolución  de mercancía del almacén "+str(almacen.name)+".<br>"
                    body += 'El producto a devolver es:<br>'
                    for line in self.move_line_ids_without_package:
                        body+= str(line.product_id.name)+" con la cantidad de "+str(line.product_uom_qty)+" piezas.<br>"

                    template_obj = self.env['mail.mail']
                    template_data = {
                        'subject': 'Solicitud de devolución de ' + self.env.user.name,
                        'body_html': body,
                        'email_from': self.env.user.company_id.email,
                        'email_to': usuario.partner_id.email
                    }
                    _logger.info("Picking:: Enviamos email con %s", template_data)
                    template_id = template_obj.sudo().create(template_data)
                    template_id.send()
                    _logger.info("Picking:: Enviado %s", template_data)
        if not gerente_encontrado:
            raise ValidationError("Advertencia, No hay un gerente asignado para aprobar en el almacen %s", self.picking_type_id.warehouse_id.name)


