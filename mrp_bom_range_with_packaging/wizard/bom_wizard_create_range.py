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
    bom_product_net_weight = fields.Float(
        string="BoM Product Net Weight",
        compute="_compute_bom_product_net_weight",
        inverse="_inverse_bom_product_net_weight",
    )

    # TODO : comment gérre faire comprendre les liens déjàfaits entre article et bom

    @api.depends("bom_id.product_tmpl_id.net_weight")
    def _compute_bom_product_net_weight(self):
        for record in self:
            record.bom_product_net_weight = record.bom_id.product_tmpl_id.net_weight

    def _inverse_bom_product_net_weight(self):
        for record in self:
            record.bom_id.product_tmpl_id.net_weight = record.bom_product_net_weight

    range_bom_ids = fields.One2many(
        comodel_name="bom.wizard.range.bom.line",
        inverse_name="wizard_id",
        string="Actual BoM range",
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
                        "bom_and_article_to_create": True,
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
            # TODO : add on option
            old_packaging_bom_line = new_bom.bom_line_ids.filtered(
                lambda line: line.product_id == self.bom_id.packaging
            )
            if old_packaging_bom_line:
                old_packaging_bom_line.write(
                    {
                        "product_id": packaging.product_id.id,
                    }
                )
            else:
                # Add Packaging product at the end
                new_bom.bom_line_ids.create(
                    {
                        "product_id": packaging.product_id.id,
                        "bom_id": new_bom.id,
                        "sequence": 1000,
                    }
                )
            new_boms.append(new_bom.id)

        # Return view with this new BoMs
        result = self.env.ref("mrp.mrp_bom_form_action").read()[0]
        result["domain"] = [("id", "in", new_boms)]
        return result
