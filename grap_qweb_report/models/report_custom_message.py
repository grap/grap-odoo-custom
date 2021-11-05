# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ReportCustomMessage(models.Model):
    _name = "report.custom.message"
    _description = "Report Custom Messages"

    name = fields.Char(required=True)

    height = fields.Float(
        string="Height",
        default="30",
        required=True,
        help="Height of the message, expressed in pixel"
    )

    border = fields.Float(
        string="Border",
        default="1",
        help="Size of the border, expressed in pixel"
    )

    company_id = fields.Many2one(comodel_name="res.company", string="Company")

    display_on_account_invoice = fields.Boolean(default=True)

    display_on_purchase_order = fields.Boolean(default=True)

    display_on_sale_order = fields.Boolean(default=True)

    display_on_stock_picking = fields.Boolean(default=True)

    background_color = fields.Char(
        string="Color",
    )

    html_text = fields.Text(string="HTML Text", required=True)

    html_text_code = fields.Text(
        string="HTML Text (Code View)",
        related="html_text",
        readonly=False
    )

    extra_css_code = fields.Char(string="Extra Css Code")

    message = fields.Text(compute="_compute_message")

    @api.depends(
        "html_text",
        "html_text_code",
        "background_color",
        "height",
        "border",
        "extra_css_code"
    )
    def _compute_message(self):
        for item in self:
            vals = {x: item[x] for x in item._fields}
            item.message = "<div style='"\
                "overflow: hidden;"\
                "width: 100%;"\
                "height: {height}px;"\
                "background-color:{background_color};"\
                "border:{border}px solid;"\
                "{extra_css_code};"\
                "'>{html_text}</div>"\
                .format(**vals)
