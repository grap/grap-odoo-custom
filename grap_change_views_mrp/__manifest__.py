# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Change Views MRP",
    "version": "12.0.1.2.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "purchase",
        "sale_mrp",
        # OCA
        "mrp_bom_note",
        "web_widget_numeric_step",
        "mrp_bom_widget_section_and_note_one2many",
        # GRAP
        "mrp_food",
        "mrp_business",
        "mrp_bom_product_variant",
        "mrp_bom_tag",
        "mrp_bom_line_has_bom",
        "mrp_bom_line_net_qty",
    ],
    "data": [
        "views/view_mrp_bom.xml",
        "views/menu.xml",
        "views/assets.xml",
    ],
    "installable": True,
}
