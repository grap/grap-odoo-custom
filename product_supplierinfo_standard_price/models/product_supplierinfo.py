# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from odoo.addons import decimal_precision as dp


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    product_standard_price = fields.Float(
        string="Product actual standard price",
        compute="_compute_product_standard_price",
    )

    theoritical_standard_price = fields.Float(
        string="Supplier info price with discount",
        compute="_compute_theoritical_standard_price",
    )

    diff_supplierinfo_product_standard_price = fields.Float(
        digits=dp.get_precision("Product Price"),
        compute="_compute_diff_supplierinfo_product_standard_price",
    )

    #
    # Other functions
    #
    @api.multi
    @api.depends("product_id", "product_id.standard_price")
    def _compute_product_standard_price(self):
        for supplierinfo in self:
            supplierinfo.product_standard_price = (
                supplierinfo.product_tmpl_id.standard_price
            )

    @api.multi
    @api.depends(
        "price",
        "discount",
        "discount2",
        "discount3",
        "currency_id",
        "product_id",
        "product_tmpl_id",
    )
    def _compute_theoritical_standard_price(self):
        for supplierinfo in self:
            uom = (
                supplierinfo.product_uom
                or supplierinfo.product_tmpl_id.uom_po_id
                or supplierinfo.product_id.uom_po_id
            )
            currency = supplierinfo.currency_id
            destination_uom = (
                supplierinfo.product_tmpl_id.uom_id or supplierinfo.product_id.uom_id
            )
            if uom and currency and destination_uom:
                supplierinfo.theoritical_standard_price = currency.round(
                    uom._compute_price(
                        (
                            supplierinfo.price
                            * (1 - supplierinfo.discount / 100)
                            * (1 - supplierinfo.discount2 / 100)
                            * (1 - supplierinfo.discount3 / 100)
                        ),
                        destination_uom,
                    )
                )

    @api.multi
    @api.depends(
        "price", "discount", "discount2", "discount3", "product_standard_price"
    )
    def _compute_diff_supplierinfo_product_standard_price(self):
        for supplierinfo in self.filtered(lambda x: x.product_tmpl_id):
            supplierinfo.diff_supplierinfo_product_standard_price = (
                supplierinfo.product_standard_price
                - supplierinfo.theoritical_standard_price
            )

    # Functions to change product fields
    @api.multi
    def set_product_standard_price_from_supplierinfo(self):
        for supplierinfo in self.filtered(lambda x: x.product_tmpl_id):
            old_product_standard_price = supplierinfo.product_tmpl_id.standard_price
            # Set new standard_price
            supplierinfo.product_tmpl_id.standard_price = (
                supplierinfo.theoritical_standard_price
            )
            diff_percentage = (
                (
                    supplierinfo.product_tmpl_id.standard_price
                    - old_product_standard_price
                )
                / old_product_standard_price
                * 100
                if old_product_standard_price != 0
                else 100
            )
            diff_percentage_str = str(round(diff_percentage, 1)) + "%"
            self.env.user.notify_success(
                message=(_("Price difference : %s") % (diff_percentage_str,)),
                title=(
                    _("New standard price for %s") % supplierinfo.product_tmpl_id.name
                ),
            )
