# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResCompanyCategory(models.Model):
    _inherit = "res.company.category"

    # Overwrite default function to filter only active and displayed companies
    @api.depends(
        "company_ids.is_displayed_in_directory",
        "company_ids.active",
        "company_ids.category_id",
        "child_ids.company_qty",
    )
    def _compute_company_qty(self):
        for category in self:
            if category.type == "normal":
                category.company_qty = len(
                    category.company_ids.filtered(
                        lambda x: x.active and x.is_displayed_in_directory
                    )
                )
            else:
                category.company_qty = sum(category.mapped("child_ids.company_qty"))
