# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP Custom - Change eMail",
    "summary": "Change default email template for invoices, "
    " sale and purchase orders",
    "version": "12.0.1.0.1",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "sale",
        "sale_recovery_moment",
    ],
    "data": [
        "data/mail_message_subtype.xml",
        "data/mail_template.xml",
        "views/view_mail_template.xml",
    ],
    "installable": True,
}
