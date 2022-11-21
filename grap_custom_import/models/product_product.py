# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models

from ..tools import tools_generic, tools_product

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Fields Section
    grap_import_supplier_name = fields.Char(
        string="Supplier Name (For import)", store=False
    )
    grap_import_supplier_product_code = fields.Char(
        string="Product Code - Supplier (For import)", store=False
    )
    grap_import_supplier_product_name = fields.Char(
        string="Product Name - Supplier (For import)", store=False
    )
    grap_import_supplier_gross_price = fields.Monetary(
        string="Product Gross Price - Supplier (For import)", store=False
    )
    grap_import_supplier_discount_1 = fields.Char(
        string="Product Discount n°1 - Supplier (For import)", store=False
    )
    grap_import_supplier_discount_2 = fields.Char(
        string="Product Discount n°2 - Supplier (For import)", store=False
    )
    grap_import_supplier_uom_purchase_qty = fields.Float(
        string="Invoice Qty - Supplier (For import)", store=False
    )
    grap_import_supplier_uom_packaging_qty = fields.Float(
        string="Packaging Qty - Supplier (For import)", store=False
    )
    grap_import_label_1 = fields.Char(string="Label n°1 (For import)", store=False)
    grap_import_label_2 = fields.Char(string="Label n°2 (For import)", store=False)
    grap_import_label_3 = fields.Char(string="Label n°3 (For import)", store=False)

    grap_import_fiscal_classification = fields.Char(
        string="Fiscal Classification (For import)", store=False
    )
    grap_import_margin_classification = fields.Char(
        string="Margin (%) (For import)", store=False
    )
    grap_import_qty_on_hand = fields.Float(
        string="Quantity on Hand (For import)", store=False
    )
    grap_import_qty_to_purchase = fields.Float(
        string="Quantity to Purchase (For import)", store=False
    )

    # Overload Section
    def _load_records_create(self, vals_list):
        new_vals_list = []
        for vals in vals_list:
            new_vals = vals.copy()
            new_vals = tools_product._handle_product_name(self, new_vals)
            new_vals = tools_product.handle_supplier_info_values(self, new_vals)
            new_vals = tools_product._handle_label_ids(self, new_vals)
            new_vals = tools_product._guess_extra_values(self, new_vals)
            new_vals = tools_generic._remove_technical_keys(new_vals)
            new_vals_list.append(new_vals)
        products = super()._load_records_create(new_vals_list)
        return products

    @api.model
    def create(self, vals):
        _logger.info("====================================")
        _logger.info(vals)
        _logger.info("====================================")
        return super().create(vals)
