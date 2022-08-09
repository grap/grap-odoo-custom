# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    ########## TIME
    time_to_produce_line = fields.Float(
        string="Time (min)",
        compute="_compute_time_to_produce_line",
        inverse="_inverse_time_to_produce_line",
        store=True,
    )
    # time_to_produce_line_theorical = fields.Float(
    #     string="Time theorical",
    #     compute="_compute_time_to_produce_line_theorical",
    # )
    time_to_produce_per_unit = fields.Float(
        string="Theorical time per unit",
        related="product_id.time_to_produce_product",
    )

    # Question : Le faire dépendre de product_id.time_to_produce_product ? Peut que ça modifie
    # des trucs en arrière plan et que ça soit pas intuitif ??
    @api.depends(
        "product_id",
        "product_id.time_to_produce_product",
        "product_qty",
        "time_to_produce_per_unit",
    )
    def _compute_time_to_produce_line(self):
        for bomline in self:
            # print("========= COMPUTE")
            bomline.time_to_produce_line = (
                bomline.time_to_produce_per_unit * bomline.product_qty
            )

    # @api.depends("product_id", "product_id.time_to_produce_product", "product_qty", "time_to_produce_per_unit")
    # def _compute_time_to_produce_line_theorical(self):
    #     for bomline in self:
    #         bomline.time_to_produce_line = bomline.time_to_produce_per_unit * bomline.product_qty

    def _inverse_time_to_produce_line(self):
        for bomline in self:
            # bomline.write({'time_to_produce_line' : bomline.time_to_produce_line})
            # import pdb; pdb.set_trace()
            # print("========= INVERSE")
            return True

    # TODO : faire un notify user quand on change dans le product la quantité ? ou mieux, écire en dessous les fiches qui seront impactés ? ou osef ?
