# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from .product_product import _PRODUCT_CODE_GENERIC_TLA


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    # ========== Divers
    currency_id = fields.Many2one(related="product_tmpl_id.currency_id")
    description_packaging = fields.Char(string="Packaging description")
    description_short = fields.Char(string="Short description")
    description_long = fields.Text(string="Long description")
    # Tracking not possible for One2many
    # bom_line_ids = fields.One2many(track_visibility="onchange")
    priority = fields.Selection(
        [("0", "Low"), ("1", "Normal"), ("2", "High"), ("3", "Very High")],
        string="Priority",
        default="0",
        help="Helps prioritize BoM.",
    )
    meal_category_id = fields.Many2one(
        related="product_id.meal_category_id",
        string="Meal category",
    )
    # ========== Fields related to weight
    bom_components_total_weight = fields.Float(
        string="Bom Components Total Weight",
        compute="_compute_bom_components_total_weight",
    )

    # ========== Code and Trigram (Three Letter Acronym)
    tla_to_change = fields.Boolean(related="product_id.tla_to_change")

    code_nb = fields.Integer(
        string="Bill Of Material Numbering",
        help="You can change it manually here and it will change reference.",
        store=True,
    )
    code = fields.Char(
        string="Reference ℹ️",
        compute="_compute_proposal_code",
        help="Code of the BoM, composed of the trigram of your activity, the "
        "trigram of the product (which can be modified on its form) and a unique number",
        store=True,
    )

    # ========== Methods for Time
    time_to_produce = fields.Float(
        help="Set this time or calculate it with BoM lines time", store=True
    )

    # Overload Section
    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        code_nb = self._get_code_nb()
        default["code_nb"] = code_nb
        return super().copy(default)

    # ========== Methods for Code and Trigram (Three Letter Acronym)
    # _get_bom_code_start → returns "BOM-COMPANYCODE-TLA"
    @api.multi
    def _get_bom_code_start(self):
        self.ensure_one()
        if not self.product_id:
            return 0
        else:
            bom_code_start = ""
            if self.env.user.company_id.code:
                bom_code_start += self.env.user.company_id.code
            if not self.product_id.tla:
                self.product_id.write({"tla": _PRODUCT_CODE_GENERIC_TLA})
                self.product_id.write({"tla_to_change": True})
                self.env.user.notify_warning(
                    message=(
                        _("You need to change default trigram on product set to %s.")
                    )
                    % (_PRODUCT_CODE_GENERIC_TLA),
                    title=(_("No Trigram on product %s ") % self.product_id.name),
                    sticky=False,
                )
            bom_code_start += ("-") + self.product_id.tla
            return bom_code_start

    def _get_code_nb(self):
        # Count archive and active BoMs
        # From the product form with the product already selected
        if self.id:
            count = (
                self.env["mrp.bom"]
                .with_context(active_test=False)
                .search_count(
                    [
                        ("product_id", "=", self.product_id.id),
                        ("code", "!=", ""),
                        ("id", "!=", self.id),
                    ]
                )
            )
        # When creating a BoM (product not already selected)
        else:
            count = (
                self.env["mrp.bom"]
                .with_context(active_test=False)
                .search_count(
                    [
                        ("product_id", "=", self.product_id.id),
                        ("code", "!=", ""),
                    ]
                )
            )
        code_nb = count + 1
        return code_nb

    # _compute_proposal_code → compute "BOM-COMPANYCODE-TLA-1"
    @api.depends("product_id", "product_id.tla", "code_nb")
    def _compute_proposal_code(self):
        for bom in self.filtered(lambda x: x.product_id):
            bom.code_nb = bom._get_code_nb()
            bom.code = bom._get_bom_code_start() + ("-") + str(bom.code_nb)

    def generate_product_tla(self):
        for bom in self.filtered(lambda x: x.product_id):
            bom.product_id.generate_tla()

    # ========== Methods related to Weight
    @api.depends("bom_line_ids.line_weight")
    def _compute_bom_components_total_weight(self):
        for bom in self:
            bom.bom_components_total_weight = sum(
                bom.bom_line_ids.mapped("line_weight")
            )
