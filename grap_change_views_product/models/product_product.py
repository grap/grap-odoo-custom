# Copyright (C) 2015-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "name"

    _COMPONENT_PRODUCT_EXPENSE_ACCOUNT = "601"
    _COMPONENT_PRODUCT_INCOME_ACCOUNT = "707"

    # Columns Section
    valuation_qty_available = fields.Float(
        compute="_compute_valuation_qty_available",
        string="Valuation of Quantity on Hand",
    )

    valuation_virtual_available = fields.Float(
        compute="_compute_valuation_virtual_available",
        string="Valuation of Virtual Quantity",
    )

    # Overload Column Section
    standard_price = fields.Float(copy=True)

    # Compute Section
    @api.multi
    def _compute_valuation_qty_available(self):
        for product in self:
            product.valuation_qty_available = (
                product.qty_available * product.standard_price
            )

    @api.multi
    def _compute_valuation_virtual_available(self):
        for product in self:
            product.valuation_virtual_available = (
                product.virtual_available * product.standard_price
            )

    # Useful for accessing product in inline tree views
    def see_current_product(self):
        self.ensure_one()
        result = self.env.ref(
            "grap_change_views_product.action_product_product"
        ).read()[0]
        form_view = self.env.ref("grap_change_views_product.view_product_product_form")
        result["views"] = [(form_view.id, "form")]
        result["res_id"] = self.id
        result["context"] = {
            "form_view_initial_mode": "edit",
        }
        return result

    @api.depends(
        "bom_line_ids",
        "categ_id.global_property_account_expense_categ",
        "categ_id.global_property_account_income_categ",
    )
    @api.multi
    def _compute_is_component_intermediate(self):
        for product in self:
            super()._compute_is_component_intermediate()
            if not product.is_component:
                # Products in 601 Account Expense are also components products
                product.is_component = (
                    product.categ_id.global_property_account_expense_categ
                    == self._COMPONENT_PRODUCT_EXPENSE_ACCOUNT
                    and product.categ_id.global_property_account_income_categ
                    == self._COMPONENT_PRODUCT_INCOME_ACCOUNT
                )
