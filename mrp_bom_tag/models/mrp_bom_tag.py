# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MrpBomTag(models.Model):
    _name = "mrp.bom.tag"
    _description = "Bill Of Material Tag"
    _parent_name = "parent_id"
    _parent_store = True
    _order = "complete_name"

    # Column Section
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda s: s._default_company_id(),
    )

    name = fields.Char(string="Name", required=True)
    complete_name = fields.Char(
        "Complete Name", compute="_compute_complete_name", store=True
    )

    parent_id = fields.Many2one(
        "mrp.bom.tag", "Parent BoM Tag", index=True, ondelete="cascade"
    )
    parent_path = fields.Char(index=True)
    child_id = fields.One2many("mrp.bom.tag", "parent_id", "Child Categories")

    color = fields.Integer("Color Index", default=0)

    bom_ids = fields.Many2many(
        comodel_name="mrp.bom",
        inverse_name="bom_tag_ids",
    )

    bom_qty = fields.Integer(
        "BoM Quantity",
        compute="_compute_bom_qty",
        help="Number of BoMs under this BoM tag (not considering children categories)",
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for bom_tag in self:
            if bom_tag.parent_id:
                bom_tag.complete_name = "%s / %s" % (
                    bom_tag.parent_id.complete_name,
                    bom_tag.name,
                )
            else:
                bom_tag.complete_name = bom_tag.name

    @api.depends("bom_ids")
    def _compute_bom_qty(self):
        for bom_tag in self:
            bom_tag.bom_qty = len(bom_tag.bom_ids)

    @api.constrains("parent_id")
    def _check_bom_tag_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive bom tags."))
        return True

    # Model Section
    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    # Name Section
    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get("display_complete_name", False):
                result.append((record.id, record.complete_name))
            else:
                result.append((record.id, record.name))
        return result
