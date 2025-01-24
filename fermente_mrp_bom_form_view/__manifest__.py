# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Fermente - MRP BoM Form View",
    "version": "16.0.1.0.1",
    "category": "Web",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # OCA
        "web_widget_numeric_step",
        "mrp_bom_widget_section_and_note_one2many",
        "mrp_bom_produce_delay_in_hour",
        # GRAP
        "mrp_bom_tag",
        "mrp_bom_line_net_qty",
        "mrp_bom_product_price_margin",
    ],
    "data": [
        "views/view_mrp_bom.xml",
    ],
}
