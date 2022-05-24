# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP - MRP technical module for development",
    "summary": "Install all MRP modules for Grap",
    "version": "12.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "purchase",
        "sale_mrp",
        "mrp_bom_note",
        # GRAP
        "grap_change_views_mrp",
        "mrp_food",
        # OCA Modules
        "mrp_bom_widget_section_and_note_one2many",
    ],
    "installable": True,
}
