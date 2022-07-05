# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    currency_id = fields.Many2one(related="product_tmpl_id.currency_id")
    image = fields.Binary(related="product_tmpl_id.image")

    # override product_uom_id to make it related to product uom
    # as it's related to product_id and required, module depends mrp_bom_product_variant
    product_uom_id = fields.Many2one(
        "uom.uom",
        "Product Unit of Measure",
        related="product_id.uom_id",
        oldname="product_uom",
        required=True,
    )

    # Code and Trigram (Three Letter Acronym)
    BOM_CODE_SEQ_START = _("BOM")
    PRODUCT_CODE_GENERIC_TLA = fields.Char(
        related="product_id.PRODUCT_CODE_GENERIC_TLA"
    )
    tla_to_change = fields.Boolean(related="product_id.tla_to_change")

    code_nb = fields.Integer(
        string="Bill Of Material Numbering",
        help="You can change it manually here and it will change reference.",
        compute="_compute_code_nb",
        inverse="_inverse_code_nb",
        store=True,
    )
    code = fields.Char(
        compute="_compute_proposal_code",
        help="Automatic code. You can change number manually"
        " or product trigram directly on product form",
        store=True,
    )

    # TODO : Handling time

    # Models methods
    # _get_bom_code_start → returns "BOM-COMPANYCODE-TLA"
    @api.multi
    def _get_bom_code_start(self):
        self.ensure_one()
        if not self.product_id:
            return 0
        else:
            bom_code_start = self.BOM_CODE_SEQ_START
            if self.env.user.company_id.code:
                bom_code_start += ("-") + self.env.user.company_id.code
            if not self.product_id.tla:
                self.product_id.write({"tla": self.PRODUCT_CODE_GENERIC_TLA})
                self.product_id.write({"tla_to_change": True})
                self.env.user.notify_warning(
                    message=_(
                        "You need to change default trigram on product set to %s."
                    )
                    % (self.PRODUCT_CODE_GENERIC_TLA),
                    title=_("No Trigram on product %s " % self.product_id.name),
                    sticky=False,
                )
            bom_code_start += ("-") + self.product_id.tla
            return bom_code_start

    @api.depends("product_id")
    def _compute_code_nb(self):
        for bom in self:
            # count archive and active BoMs
            count = (
                self.env["mrp.bom"]
                .with_context(active_test=False)
                .search_count(
                    [
                        ("product_id", "=", bom.product_id.id),
                        ("code", "!=", ""),
                    ]
                )
            )
            bom.code_nb = count + 1

    def _inverse_code_nb(self):
        return True

    # _compute_proposal_code → compute "BOM-COMPANYCODE-TLA-1"
    @api.depends("product_id.tla", "code_nb")
    def _compute_proposal_code(self):
        for bom in self.filtered(lambda x: x.product_id):
            bom.code = bom._get_bom_code_start() + ("-") + str(bom.code_nb)

    def generate_product_tla(self):
        for bom in self.filtered(lambda x: x.product_id):
            bom.product_id.generate_tla()
