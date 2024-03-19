# Copyright (C) 2024-Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP BoM Weight",
    "version": "12.0.1.1.1",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # GRAP modules
        "mrp_bom_line_net_qty",
    ],
    "data": [
        "views/view_mrp_bom.xml",
    ],
    "installable": True,
}
