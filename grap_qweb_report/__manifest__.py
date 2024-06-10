# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Custom Qweb Reports",
    "version": "12.0.2.2.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "purchase",
        "point_of_sale",
        "l10n_fr",
        # OCA
        "pos_ticket_extra_company_info",
        "pos_ticket_extra_company_info_l10n_fr",
        "purchase_triple_discount",
        "report_xlsx_helper",
        # GRAP
        "base_company_legal_info",
        "fiscal_company_base",
        "stock_inventory_valuation",
        # Coop It Easy
        "pos_customer_wallet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/view_report_custom_message.xml",
        "report/qweb_template_product_product_barcode.xml",
        "report/qweb_template_layout_standard.xml",
        "report/qweb_template_account_invoice.xml",
        "report/qweb_template_purchase_order.xml",
        "report/qweb_template_sale_order.xml",
        "report/qweb_template_stock_picking.xml",
        "report/qweb_template_stock_inventory.xml",
        "data/report_paperformat.xml",
        "data/ir_actions_report_xml.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/report_custom_message.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    "external_dependencies": {"python": ["slugify"]},
    "installable": True,
}
