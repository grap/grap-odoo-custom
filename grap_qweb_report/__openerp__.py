# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'GRAP - Custom Qweb Reports',
    'version': '8.0.1.0.0',
    'category': 'GRAP - Custom',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'base_fiscal_company',
        'l10n_fr_siret',
        'purchase',
        'sale',
        'sale_recovery_moment',
        'sale_food',
        'product_ean13_image',
        'product_print_category',
        'point_of_sale',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'report/qweb_template_layout.xml',
        'report/qweb_template_account_invoice.xml',
        'report/qweb_template_picking_summary_wizard.xml',
        'report/qweb_template_purchase_order.xml',
        'report/qweb_template_purchase_order_quotation.xml',
        'report/qweb_template_sale_order.xml',
        'report/qweb_template_stock_picking.xml',
        'report/qweb_template_product_product.xml',
        'report/ir_actions_report_xml.xml',
        'views/action.xml',
        'views/menu.xml',
        'views/templates.xml',
        'views/view_picking_summary_wizard.xml',
        'views/view_res_company.xml',
        'views/view_product_uom.xml',
        'views/view_product_pricetag_type.xml',
        'views/view_product_product.xml',
        'views/view_stock_picking.xml',
        'data/product_print_category.xml',
    ],
    'qweb': [
        'static/src/xml/grap_qweb_report.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/product_uom.xml',
        'demo/product_pricetag_type.xml',
        'demo/product_product.xml',
        'demo/product_print_category.xml',
    ],
}
