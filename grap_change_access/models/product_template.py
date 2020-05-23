# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Constraint section
    @api.constrains("expense_pdt", "income_pdt")
    def _check_pos_ok_res_group(self):
        if self.env.user.has_group("account.group_account_manager"):
            return
        if self.filtered(lambda x: x.expense_pdt or x.income_pdt):
            raise ValidationError(
                _(
                    "You can not create an POS expense or income product"
                    " if you're not account manager !"
                )
            )

    @api.constrains("expense_pdt", "income_pdt", "sale_ok", "purchase_ok")
    def _check_purchase_sale_pos_ok(self):
        for product in self.filtered(lambda x: x.expense_pdt or x.income_pdt):
            if product.sale_ok or product.purchase_ok:
                raise ValidationError(
                    _(
                        "You can not create a product that is both salable or"
                        " purchasable and POS expense or income product !"
                    )
                )

    @api.constrains(
        "expense_pdt",
        "income_pdt",
        "property_account_expense",
        "property_account_income",
    )
    def _check_pos_property_account(self):
        for product in self.filtered(lambda x: x.expense_pdt):
            if not product.property_account_expense:
                raise ValidationError(
                    _(
                        "You can not create an POS expense product without account"
                        " expense !"
                    )
                )
        for product in self.filtered(lambda x: x.income_pdt):
            if not product.property_account_income:
                raise ValidationError(
                    _(
                        "You can not create an POS income product without account"
                        " income !"
                    )
                )
