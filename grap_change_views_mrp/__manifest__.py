# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - Change Views MRP",
    "version": "12.0.1.1.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "purchase",
        "sale_mrp",
        # "mrp_bom_cost",
        # OCA
        # "mrp_bom_component_menu",
        # "mrp_auto_assign",
        "mrp_bom_note",
        # "mrp_bom_tracking",
        # "mrp_production_grouped_by_product",
        # "mrp_production_note",
        # "mrp_warehouse_calendar",
        # "product_mrp_info",
        "web_widget_numeric_step",
        "mrp_bom_widget_section_and_note_one2many",
        # GRAP
        "mrp_food",
    ],
    "data": [
        "security/res_groups.xml",
        "views/menu.xml",
        "views/view_mrp_bom.xml",
    ],
    "installable": True,
}