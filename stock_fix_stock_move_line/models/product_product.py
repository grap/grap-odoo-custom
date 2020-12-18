# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import api, fields, models


logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    fix_stock_move_lines_state = fields.Selection(
        string="Fix Stock Move Lines State",
        default="todo", selection=[
            ("todo", "To Do"),
            ("done", "Done"),
            ("fixed_1", "Fixed (1)"),
            ("fixed_2", "Fixed (2)"),
            ("fixed_3", "Fixed (3)"),
            ("fixed_4", "Fixed (4)"),
            ("fixed_5", "Fixed (5)"),
            ("fixed_6", "Fixed (6)"),
            ("fixed_7", "Fixed (7)"),
        ])

    @api.model
    def _fix_stock_move_line_cron(self, limit):
        date_begin = fields.datetime.now()
        products = self.sudo().with_context(active_test=False).search([
            ('fix_stock_move_lines_state', '=', "todo"),
        ], limit=limit)
        products.button_fix_stock_move_line()
        date_end = fields.datetime.now()
        logger.info(
            "Fixed Stock move lines for %s products in %s"
            ". Average time %s" % (
                len(products), str(date_end - date_begin),
                str((date_end - date_begin) / len(products))
            ))

    @api.multi
    def button_fix_stock_move_line(self):
        for product in self:
            logger.info("Handle %s-%s" % (product.default_code, product.name))
            state = 'done'

            quants = self.env["stock.quant"].search(
                [('product_id', '=', product.id)])
            move_line_ids = []
            for quant in quants:
                move_lines = self.env["stock.move.line"].search(
                    [
                        ("product_id", "=", quant.product_id.id),
                        ("location_id", "=", quant.location_id.id),
                        ("lot_id", "=", quant.lot_id.id),
                        ("package_id", "=", quant.package_id.id),
                        ("owner_id", "=", quant.owner_id.id),
                        ("product_qty", "!=", 0),
                    ]
                )

                move_line_ids += move_lines.ids
                reserved_on_move_lines = sum(move_lines.mapped("product_qty"))

                if quant.location_id.should_bypass_reservation():
                    # If a quant is in a location that should bypass the
                    # reservation, its `reserved_quantity` field
                    # should be 0.
                    if quant.reserved_quantity != 0:
                        state = 'fixed_1'
                        quant.write({"reserved_quantity": 0})
                else:
                    # If a quant is in a reservable location, its
                    # `reserved_quantity` should be exactly the sum
                    # of the `product_qty` of all the partially_available
                    # / assigned move lines with the same
                    # characteristics.
                    if quant.reserved_quantity == 0:
                        if move_lines:
                            state = 'fixed_2'
                            move_lines.with_context(bypass_reservation_update=True).write(
                                {"product_uom_qty": 0}
                            )

                    elif quant.reserved_quantity < 0:
                        state = 'fixed_3'
                        quant.write({"reserved_quantity": 0})
                        if move_lines:
                            move_lines.with_context(bypass_reservation_update=True).write(
                                {"product_uom_qty": 0}
                            )
                    else:
                        if reserved_on_move_lines != quant.reserved_quantity:
                            state = 'fixed_4'
                            move_lines.with_context(bypass_reservation_update=True).write(
                                {"product_uom_qty": 0}
                            )
                            quant.write({"reserved_quantity": 0})
                        else:
                            if any(move_line.product_qty < 0 for move_line in move_lines):
                                state = 'fixed_5'
                                move_lines.with_context(bypass_reservation_update=True).write(
                                    {"product_uom_qty": 0}
                                )
                                quant.write({"reserved_quantity": 0})
            move_lines = self.env["stock.move.line"].search(
                [
                    ("product_id", "=", product.id),
                    ("product_qty", "!=", 0),
                    ("id", "not in", move_line_ids),
                ]
            )
            move_lines_to_unreserve = []
            for move_line in move_lines:
                if not move_line.location_id.should_bypass_reservation():
                    move_lines_to_unreserve.append(move_line.id)

            if len(move_lines_to_unreserve) > 1:
                state = 'fixed_6'
                self.env.cr.execute(
                    """
                        UPDATE stock_move_line
                        SET product_uom_qty = 0, product_qty = 0
                        WHERE id in %s;
                    """
                    % (tuple(move_lines_to_unreserve),)
                )
            elif len(move_lines_to_unreserve) == 1:
                state = 'fixed_7'
                self.env.cr.execute(
                    """
                    UPDATE stock_move_line
                    SET product_uom_qty = 0, product_qty = 0
                    WHERE id = %s ;
                    """
                    % (move_lines_to_unreserve[0])
                )

            product.fix_stock_move_lines_state = state

    # _name = 'stock.quant'

    # @api.model
    # def _update_reserved_quantity(
    #         self, product_id, location_id, quantity, lot_id=None,
    #         package_id=None, owner_id=None, strict=False
    #     ):
    #     try:
    #         return super()._update_reserved_quantity(
    #             product_id, location_id, quantity,
    #             lot_id=lot_id, package_id=package_id,
    #             owner_id=owner_id, strict=strict)

    #     except UserError:
    #         logger.warning("on corrige manuellement")
    #         product = self.env["product.product"].browse(product_id)
    #         product.button_fix_stock_move_line()

    #     return super()._update_reserved_quantity(
    #         product_id, location_id, quantity,
    #         lot_id=lot_id, package_id=package_id,
    #         owner_id=owner_id, strict=strict)
