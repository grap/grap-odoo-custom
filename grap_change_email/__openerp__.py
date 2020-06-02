# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "GRAP Custom - Change eMail",
    "version": "8.0.4.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": ["purchase", "sale", "sale_recovery_moment", "email_template",],
    "data": [
        "data/email_template.xml",
        "views/view_mail_compose_message.xml",
    ],
    "installable": False,
}
