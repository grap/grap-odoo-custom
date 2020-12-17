# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from openupgradelib import openupgrade_merge_records


QUANT_MERGE_OPS = {
    # The rest of the values are good with default merge operation
    'in_date': 'min',
    'removal_date': 'max',
}

logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    quant_merged_state = fields.Selection(
        string="Quant Merge State",
        default="todo", selection=[
            ("todo", "To Do"),
            ("done", "Done"),
            ("error", "Error"),
        ])

    @api.model
    def _quant_merge_cron(self, limit):
        date_begin = fields.datetime.now()
        products = self.sudo().search(
            [('quant_merged_state', '=', "todo")],
            limit=limit
        )
        products.button_quant_merge()
        date_end = fields.datetime.now()
        logger.info("Merged quant for %s products in %s. Average time %s" % (
            len(products), str(date_end - date_begin),
            str((date_end - date_begin) / len(products))
        ))

    @api.multi
    def button_quant_merge(self):
        count = 0
        for product in self:
            count += 1
            group_list = [
                'product_id', 'package_id', 'lot_id', 'location_id',
                'owner_id',
            ]
            StockQuant = self.env['stock.quant']
            groups = StockQuant.read_group(
                [('product_id', '=', product.id)],
                group_list, group_list, lazy=False
            )
            has_error = False
            for group in groups:
                quants = StockQuant.search(group['__domain'])
                if len(quants) == 1:
                    continue
                try:
                    with self.env.cr.savepoint():
                        openupgrade_merge_records.merge_records(
                            self.sudo().env, 'stock.quant', quants[1:].ids,
                            quants[0].id,
                            QUANT_MERGE_OPS,
                        )
                except ValidationError as error:
                    has_error = True
                    logger.error(
                        'Cannot merge quants %s for '
                        'product %s, package %s, lot %s, '
                        'location %s, owner %s: %s',
                        quants.ids,
                        quants[0].product_id.default_code
                        or quants[0].product_id.name,
                        quants[0].package_id.name or '-',
                        quants[0].lot_id.name or '-',
                        quants[0].location_id.complete_name,
                        quants[0].owner_id.name or '-',
                        error,
                    )
            if has_error:
                product.quant_merged_state = "error"
            else:
                product.quant_merged_state = "done"
