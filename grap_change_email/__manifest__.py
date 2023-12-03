# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP Custom - Change eMail",
    "summary": "Change default email template for invoices, "
    " sale and purchase orders",
    "version": "12.0.1.1.5",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-custom",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "sale",
        # OCA
        "mail_template_multi_attachment",
        # GRAP
        "sale_recovery_moment",
        "grap_qweb_report",
    ],
    "data": [
        "data/mail_data.xml",
        "data/mail_message_subtype.xml",
        "data/mail_template.xml",
        "views/view_mail_template.xml",
    ],
    "installable": True,
}
