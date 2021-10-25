# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "GRAP - Change Mail Views",
    "version": "12.0.1.1.2",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        "views/templates.xml",
        "views/view_account_invoice_send.xml",
        "views/view_mail_compose_message.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
