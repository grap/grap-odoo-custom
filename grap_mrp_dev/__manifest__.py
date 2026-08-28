# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - MRP technical module for development",
    "summary": "Install all MRP modules for Grap",
    "version": "16.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # OCA
        "mrp_bom_widget_section_and_note_one2many",
        "mrp_bom_line_net_qty",
        "mrp_bom_simple_report",
        "mrp_bom_product_price_margin",
        "mrp_bom_tag",
        "mrp_bom_select_product_variant",
        "mrp_bom_order_by_product_name",
        "mrp_bom_produce_delay",
        "mrp_product_produce_delay_in_hour",
        "mrp_bom_produce_delay_in_hour",
        "mrp_bom_image",
        "mrp_product_characterisation",
    ],
    "installable": True,
}
