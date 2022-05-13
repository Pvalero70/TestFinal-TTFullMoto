import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError, Warning

_logger = logging.getLogger(__name__)


class RepairMechanic(models.Model):
    _name = 'repair.mechanic'

    _description = "Model that saves contact of mechanics"
    _rec_name = 'name_computed'

    _sql_constraints = [
        ('numero_tecnico_unique', 'unique(numero_tecnico)', 'No puedes duplicar el numero de tecnico')
    ]

    name_computed = fields.Char(string="Computado", compute='_compute_name',store=True)

    first_name = fields.Char("Primer nombre",required=1)
    second_name = fields.Char("Segundo nombre")
    first_ap = fields.Char("Primer apellido", required=1)
    second_ap = fields.Char("Segundo apellido")
    numero_tecnico = fields.Char("Numero de tecnico")
    location_id = fields.Many2one('stock.location',"Ubicacion")
    company_id = fields.Many2one('res.company',"Empresa",default=lambda self: self.env.company)

    @api.onchange('numero_tecnico')
    def _compute_total_customer_limit_total(self):
        existe_numero_tecnico = self.env['repair.mechanic'].search([('numero_tecnico', '=', self.numero_tecnico)])
        if existe_numero_tecnico:
            raise ValidationError(_("El numero de tecnico %s ya existe",self.numero_tecnico))



    @api.depends('first_name','second_name','first_ap','second_ap')
    def _compute_name(self):
        for rec in self:
            nombre = ''
            if rec.first_name:
                nombre = rec.first_name + " "

            if rec.second_name:
                nombre += rec.second_name + " "

            if rec.first_ap:
                nombre += rec.first_ap + " "

            if rec.second_ap:
                nombre+= rec.second_ap


            rec.name_computed = nombre


class RepairOrderInherit(models.Model):

    _inherit = 'repair.order'

    mechanic_id = fields.Many2one('repair.mechanic',"Mecanico")


