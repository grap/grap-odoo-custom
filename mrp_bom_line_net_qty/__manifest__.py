# Copyright (C) 2023-Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP BoM Line Net and Gross Quantity",
    "version": "12.0.1.1.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        # OCA modules
        "product_net_weight",
    ],
    "data": [
        "views/view_mrp_bom.xml",
    ],
    "installable": True,
}
