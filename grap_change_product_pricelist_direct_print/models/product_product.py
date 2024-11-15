# Copyright (C) 2023-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # TODO: Migration V16. This part could go in sale_eshop
    # module
    def get_eshop_description_without_paragraph(self):
        self.ensure_one()
        res = self.eshop_description
        if res.startswith("<p>"):
            res = res[3:]
        if res.endswith("</p>"):
            res = res[:-4]
        return res
