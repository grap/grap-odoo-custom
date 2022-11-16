# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import fields, models

from ..tools import tools_generic, tools_product

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Fields Section
    grap_import_supplier_name = fields.Char(string="Supplier Name", store=False)
    grap_import_supplier_product_code = fields.Char(
        string="Product Code (Supplier)", store=False
    )
    grap_import_supplier_product_name = fields.Char(
        string="Product Name (Supplier)", store=False
    )
    grap_import_supplier_gross_price = fields.Char(
        string="Product Gross Price (Supplier)", store=False
    )
    grap_import_supplier_discount_1 = fields.Char(
        string="Product Discount n°1 (Supplier)", store=False
    )
    grap_import_supplier_discount_2 = fields.Char(
        string="Product Discount n°2 (Supplier)", store=False
    )
    grap_import_supplier_uom_purchase_qty = fields.Char(
        string="Invoice Qty (Supplier)", store=False
    )
    grap_import_supplier_uom_packaging_qty = fields.Char(
        string="Packaging Qty (Supplier)", store=False
    )

    grap_import_label_1 = fields.Char(string="Label n°1", store=False)
    grap_import_label_2 = fields.Char(string="Label n°2", store=False)
    grap_import_label_3 = fields.Char(string="Label n°3", store=False)

    # Overload Section
    def _load_records_create(self, vals_list):
        _logger.info("====================================")
        _logger.info("====================================")
        _logger.info("====================================")
        _logger.info("_load_records_create")
        _logger.info("INITIAL VALUES : %d items" % len(vals_list))
        _logger.info(vals_list)
        new_vals_list = []
        for vals in vals_list:
            new_vals = vals.copy()
            new_vals = tools_product._handle_product_name(self, new_vals)
            new_vals = tools_product.handle_supplier_info_values(new_vals)
            new_vals = tools_product._handle_label_ids(self, new_vals)
            new_vals = tools_generic._remove_technical_keys(new_vals)
            new_vals_list.append(new_vals)
        _logger.info("====================================")
        _logger.info("FINAL VALUES : %d items" % len(new_vals_list))
        _logger.info(new_vals_list)
        products = super()._load_records_create(new_vals_list)
        return products
