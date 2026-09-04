# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_id = fields.Many2one(default=lambda x: x._default_category_id())

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        all_products_with_problem = res.filtered(lambda x: not x.categ_id.active)
        if all_products_with_problem:
            for category in all_products_with_problem.mapped("categ_id"):
                products = all_products_with_problem.filtered(
                    lambda x, category=category: x.categ_id == category
                )
                self.env.user.notify_warning(
                    title=_(
                        "Disabled Category for %(products_qty)d products",
                        products_qty=len(products),
                    ),
                    message=_(
                        "%(products_qty)d products has been created"
                        ' with the disabled category "%(category_name)s"'
                        " Please reaffect the following products"
                        " to a correct active category:"
                        "<br /><br />- %(product_names)s",
                        products_qty=len(products),
                        category_name=category.name,
                        product_names="<br />- ".join(products.mapped("name")),
                    ),
                    sticky=True,
                )
        return res

    def _default_category_id(self):
        # we redefine the function, (with a new name)
        # because the previous one is not overloadable,
        # and because the previous one is cached by orm.

        result = self._get_default_category_id()

        if result.active:
            # if the defaul category is active, return it
            return result

        if self.env.context.get("install_mode"):
            # In install mode, return also the default category
            # even if the category is disabled to avoid error in tests
            # and loading demo data
            return result

        if self.env.context.get("create_product_product"):
            # we are in the create section of the product.product model,
            # category has not been defined, and default value has been called
            # we avoid blocking and return result
            # In that case, a message will be displayed to the user
            # (see product.product create function)
            return result

        return False
