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

    name_computed = fields.Char(string="Computado", compute='_compute_name')

    first_name = fields.Char("Primer nombre",required=1)
    second_name = fields.Char("Segundo nombre")
    first_ap = fields.Char("Primer apellido", required=1)
    second_ap = fields.Char("Segundo apellido")
    numero_tecnico = fields.Char("Numero de tecnico")
    location_id = fields.Many2one('stock.location',"Ubicacion")
    company_id = fields.Many2one('res.company',"Empresa",default=lambda self: self.env.company)



    @api.depends('first_name','second_name','first_ap','second_ap')
    def _compute_name(self):
        for rec in self:
            nombre = rec.first_name + " "+ (str(rec.second_name+" ") if rec.second_name else "") + rec.first_ap +" "+ (str(rec.second_ap) if rec.second_ap else "")

            rec.name_computed = nombre


class RepairOrderInherit(models.Model):

    _inherit = 'repair.order'

    mechanic_id = fields.Many2one('repair.mechanic',"Mecanico")


