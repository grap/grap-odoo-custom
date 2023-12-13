# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleGroupedWizardLine(models.TransientModel):
    _name = "sale.grouped.wizard.line"
    _description = (
        "Wizard line for printing purchase list from selected bill of materials"
    )

    # Columns Section
    wizard_id = fields.Many2one(comodel_name="sale.grouped.wizard")

    sale_id = fields.Many2one(comodel_name="sale.order", string="Sale order")
    sale_partner_id = fields.Many2one(
        comodel_name="res.partner", compute="_compute_sale_partner", string="Partner"
    )

    @api.depends("sale_id")
    def _compute_sale_partner(self):
        for line in self.filtered(lambda x: x.sale_id):
            line.sale_partner_id = line.sale_id.partner_id.id
