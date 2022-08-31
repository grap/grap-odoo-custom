# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"
    _order = "sequence"

    # ========== Divers
    currency_id = fields.Many2one(related="product_tmpl_id.currency_id")
    description_packaging = fields.Char(string="Packaging description")
    description_short = fields.Char(string="Short description")
    description_long = fields.Text(string="Long description")
    # Tracking not possible for One2many
    # bom_line_ids = fields.One2many(track_visibility="onchange")

    # ========== Code and Trigram (Three Letter Acronym)
    PRODUCT_CODE_GENERIC_TLA = fields.Char(
        related="product_id.PRODUCT_CODE_GENERIC_TLA"
    )
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
    # Trop "compliqué" pour l'usage ? → remplacer par affichage de "min" aux bons endroits
    # uom_time_to_produce = fields.Many2one(
    #     comodel_name="uom.uom",
    #     domain=[("measure_type", "=", "time")]
    # )
    diff_time_to_produce_bom_and_lines = fields.Boolean(
        compute="_compute_diff_time_to_produce_bom_and_lines"
    )
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
                self.product_id.write({"tla": self.PRODUCT_CODE_GENERIC_TLA})
                self.product_id.write({"tla_to_change": True})
                self.env.user.notify_warning(
                    message=(
                        _("You need to change default trigram on product set to %s.")
                    )
                    % (self.PRODUCT_CODE_GENERIC_TLA),
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

    # ========== Methods for Time
    # Let user write by hand this time or generate thanks to this method
    def generate_proposal_bom_time(self):
        for bom in self:
            bom.time_to_produce = sum(bom.bom_line_ids.mapped("time_to_produce_line"))

    @api.depends("bom_line_ids", "time_to_produce")
    def _compute_diff_time_to_produce_bom_and_lines(self):
        for bom in self:
            time_theoric_lines = sum(bom.bom_line_ids.mapped("time_to_produce_line"))
            bom.diff_time_to_produce_bom_and_lines = (
                True if time_theoric_lines != bom.time_to_produce else False
            )
