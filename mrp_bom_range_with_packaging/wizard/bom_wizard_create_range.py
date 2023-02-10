# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BomWizardCreateRange(models.TransientModel):
    _name = "bom.wizard.create.range"
    _description = "Wizard to create range"

    # Column Section
    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        default=lambda s: s._default_bom_id(),
    )
    range_bom_ids = fields.One2many(
        comodel_name="bom.wizard.range.bom.line",
        inverse_name="wizard_id",
        string="Actual range of BoM",
        default=lambda s: s._default_range_bom_ids(),
    )
    product_packaging_ids = fields.One2many(
        comodel_name="bom.wizard.range.packaging.line",
        inverse_name="wizard_id",
        string="Products packaging lines",
        default=lambda s: s._default_product_packaging_ids(),
    )

    # Default Section
    @api.model
    def _default_bom_id(self):
        return self.env.context.get("active_id", False)

    @api.model
    def _default_range_bom_ids(self):
        bom_vals = []
        context = self.env.context
        bom_obj = self.env["mrp.bom"]
        # Get First BoM selected on which to base duplication
        bom_ids = context.get("active_ids", [])
        bom_active = bom_obj.browse(bom_ids[0])
        # Get Actual Range of BoMs
        boms = bom_obj.search([("product_tmpl_id", "=", bom_active.product_tmpl_id.id)])
        # Initialize lines
        for bom in boms:
            bom_vals.append(
                (
                    0,
                    0,
                    {
                        "bom_id": bom.id,
                        "packaging": bom.packaging,
                    },
                )
            )
        return bom_vals

    @api.model
    def _default_product_packaging_ids(self):
        product_packaging_vals = []
        context = self.env.context
        product_obj = self.env["product.product"]
        bom_obj = self.env["mrp.bom"]
        # Get First BoM selected on which to base duplication
        bom_ids = context.get("active_ids", [])
        bom_obj.browse(bom_ids[0])
        # Packagings in all BoM of this product
        product_packaging_used_ids = [
            element[2]["packaging"].id for element in self._default_range_bom_ids()
        ]
        # Get Database of products packaging without packaging already used
        product_packaging_to_use_ids = product_obj.search(
            [("is_packaging", "=", True), ("id", "not in", product_packaging_used_ids)]
        )
        # Initialize lines
        for product in product_packaging_to_use_ids:
            product_packaging_vals.append(
                (
                    0,
                    0,
                    {
                        "product_id": product.id,
                    },
                )
            )
        return product_packaging_vals

    @api.multi
    def create_bom_with_packagins(self):
        self.ensure_one()
        new_boms = []
        # Create range of BoMS
        for packaging in self.product_packaging_ids:
            new_bom = self.bom_id.copy()
            new_bom.packaging = packaging.product_id
            new_boms.append(new_bom.id)
        # Return view with this new BoMs
        result = self.env.ref("mrp.mrp_bom_form_action").read()[0]
        result["domain"] = [("id", "in", new_boms)]
        return result
