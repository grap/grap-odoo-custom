# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    _DISTRIBUTION_CHANNEL_CRITERION = [
        ("short", "Local distribution channel"),
        ("middle", "Middle distribution channel"),
        ("long", "Long distribution channel"),
    ]

    distribution_channel_criterion = fields.Selection(
        string="Distribution Channel",
        selection=_DISTRIBUTION_CHANNEL_CRITERION,
        help="* Short: artisanal producer or transformer\n"
        "* Medium: cooperative processor, producers' cooperative"
        " or importers whose only activity is to work directly"
        " with producers from other countries.\n"
        "* Long: the rest",
    )
