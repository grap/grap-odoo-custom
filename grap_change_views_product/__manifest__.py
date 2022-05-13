# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Product Views",
    "version": "12.0.0.1.14",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "product",
        "purchase",
        "sale",
        "point_of_sale",
        "stock",
        "sale_invoice_policy",
        # OCA
        "product_margin_classification",
        "product_pricelist_margin",
        "barcodes_generator_product",
        "product_form_purchase_link",
        "pos_meal_voucher",
        "pos_tare",
        "product_net_weight",
        "purchase_discount",
        "purchase_triple_discount",
        "product_standard_price_tax_included",
        "product_sale_tax_price_included",
        # GRAP
        "fiscal_company_product",
        "grap_mrp",
        "stock_preparation_category",
        "recurring_consignment",
        "product_to_scale_bizerba",
        "sale_eshop",
        "product_food",
        "product_label",
        "product_print_category",
        "product_simple_pricelist",
        "product_print_category_food_report",
        "product_origin",
        "product_origin_l10n_fr_department",
        "product_notation",
        "purchase_package_qty",
        "account_invoice_supplierinfo_update_standard_price",
        "pos_sector",
        "intercompany_trade_product",
        "joint_buying_product",
    ],
    "data": [
        "views/menu.xml",
        "views/view_product_margin_classification.xml",
        "views/view_product_pricelist.xml",
        "views/view_product_pricelist_item.xml",
        "views/view_product_supplierinfo.xml",
        "views/view_product_product_stock.xml",
        "views/view_product_product_tree.xml",
        "views/view_product_product_form.xml",
    ],
    "installable": True,
}
