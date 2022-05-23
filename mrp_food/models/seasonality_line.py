# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SeasonalityLine(models.Model):
    _name = "seasonality.line"
    _description = "Seasonality Line"

    # Column Section
    name = fields.Char(string="Seasonality line name", required=True)

    seasonality_id = fields.Many2one(
        comodel_name="seasonality",
        string="Seasonality",
    )

    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)

    @api.constrains("date_start", "date_end")
    def _check_date_end(self):
        for line in self:
            if line.date_end and line.date_end < line.date_start:
                raise ValidationError(
                    _("The end date cannot be earlier than the start date.")
                )
