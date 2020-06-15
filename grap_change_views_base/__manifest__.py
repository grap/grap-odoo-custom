# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Base Views",
    "version": "12.0.0.0.2",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "base",
        "delivery",
        "purchase",
        "sale_invoice_group_method",
        "stock",
    ],
    "data": [
        "views/view_ir_model_access.xml",
        "views/view_res_company.xml",
        "views/view_res_partner.xml",
    ],
    "installable": True,
}
