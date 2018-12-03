# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, models

from openerp.exceptions import Warning


class PosSession(models.Model):
    _inherit = "pos.session"

    # OVERWRITE Section
    @api.multi
    def _confirm_orders(self):
        """OVERWRITE _confirm_orders function (that generate sale entries)
        We so SKIP the call of
        * _create_account_move
        * _create_account_move_line
        """
        order_obj = self.env['pos.order']
        for session in self:
            # control First if order state is OK
            orders = session.order_ids.filtered(
                lambda order: order.state not in ('paid', 'invoiced'))
            if len(orders):
                raise Warning(_(
                    "The following orders are not in a paid or invoiced"
                    " status: %s") % ', '.join(
                        [order.name for order in orders]))

            # parse the orders to group the ids according to the key fields
            order_groups = {}
            for order in session.order_ids.filtered(
                    lambda order: order.state in ('paid')):
                key = (
                    order._prepare_date_sale_move_point_of_sale(),
                )
                order_groups.setdefault(key, [])
                order_groups[key].append(order.id)

            # for each group, create account_move and account_move_lines
            i = 0
            for key in order_groups.keys():
                i += 1
                orders = order_obj.browse(order_groups[key])
                move = session._create_move_point_of_sale(key, orders)
                orders.write({'account_move': move.id})
                orders.write({'state': 'done'})

    # Custom Section
    @api.multi
    def _create_move_point_of_sale(self, key, orders):
        """Generate account an account moves for the given orders, key
        and session"""
        self.ensure_one()
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']

        move_vals = self._prepare_move_point_of_sale(
            key, orders)

        move = move_obj.create(move_vals)
        product_groups = {}
        tax_groups = {}
        for order in orders:
            for line in order.lines:
                product = line.product_id

                # manage income account
                if product.property_account_income.id:
                    product_account_id = product.property_account_income.id
                elif product.categ_id.property_account_income_categ.id:
                    product_account_id =\
                        product.categ_id.property_account_income_categ.id
                else:
                    raise Warning(_(
                        "Please define income account for this product:"
                        " '%s' (id:%d).") % (product.name, product.id))

                # manage income analytic account
                product_analytic_account_id =\
                    order._prepare_analytic_account(line)

                # manage taxes
                if len(line.tax_ids) > 1:
                    raise Warning(_(
                        "Unimplemented feature, the line %s (order %s) has"
                        " more than one tax.") % (product.name, order.name))

                tax_code_id = line.tax_ids and\
                    line.tax_ids[0].base_code_id.id or False

                # 'product' lines
                product_key = (
                    product_account_id,
                    product_analytic_account_id,
                    tax_code_id,
                )
                product_groups.setdefault(product_key, [])
                product_groups[product_key].append(line.id)

                # Tax lines
                if line.tax_ids:
                    tax_key = (
                        line.tax_ids[0].id,
                    )
                    tax_groups.setdefault(tax_key, [])
                    tax_groups[tax_key].append(line.id)

        # Create 'product' lines for each key in product_groups
        for key, order_line_ids in product_groups.iteritems():
            product_line_vals = self._prepare_product_move_line_point_of_sale(
                key, order_line_ids, move)
            move_line_obj.create(product_line_vals)

        # Create 'tax' lines for each key in tax_groups
        for key, order_line_ids in tax_groups.iteritems():
            tax_line_vals = self._prepare_tax_move_line_point_of_sale(
                key, order_line_ids, move)
            move_line_obj.create(tax_line_vals)

        # create Counterpart line
        counterpart_line_vals =\
            self._prepare_counterpart_move_line_point_of_sale(orders, move)
        move_line_obj.create(counterpart_line_vals)

        # Confirm move
        move.post()
        return move

    # Prepare function
    @api.multi
    def _prepare_move_point_of_sale(self, key, orders):
        self.ensure_one()
        (date_order) = key
        period_obj = self.env['account.period']
        return {
            'journal_id': self.config_id.journal_id.id,
            'partner_id': False,
            'period_id': period_obj.find(dt=date_order).id,
            'date': date_order,
            'ref': self.name,
        }

    @api.multi
    def _prepare_product_move_line_point_of_sale(
            self, key, order_line_ids, move):
        self.ensure_one()
        account_obj = self.env['account.account']
        order_line_obj = self.env['pos.order.line']

        (account_id, analytic_account_id, tax_code_id) = key
        account = account_obj.browse(account_id)

        amount = 0
        for order_line in order_line_obj.browse(order_line_ids):
            amount += order_line.price_subtotal

        return {
            'name': account.name,
            'move_id': move.id,
            'account_id': account_id,
            'analytic_account_id': analytic_account_id,
            'credit': ((amount > 0) and amount) or 0.0,
            'debit': ((amount < 0) and - amount) or 0.0,
            'tax_code_id': tax_code_id,
            'tax_amount': amount,
        }

    @api.multi
    def _prepare_tax_move_line_point_of_sale(
            self, key, order_line_ids, move):
        self.ensure_one()
        tax_obj = self.env['account.tax']
        order_line_obj = self.env['pos.order.line']

        (tax_id) = key
        tax = tax_obj.browse(tax_id)

        amount = 0
        for order_line in order_line_obj.browse(order_line_ids):
            amount += order_line.price_subtotal_incl -\
                order_line.price_subtotal

        return {
            'name': tax.name,
            'move_id': move.id,
            'account_id': tax.account_collected_id.id,
            'credit': ((amount > 0) and amount) or 0.0,
            'debit': ((amount < 0) and - amount) or 0.0,
            'tax_code_id': tax.tax_code_id.id,
            'tax_amount': amount,
        }

    def _prepare_counterpart_move_line_point_of_sale(self, orders, move):
        self.ensure_one()
        property_obj = self.env['ir.property']
        account = property_obj.get(
            'property_account_receivable', 'res.partner')

        amount = 0
        for order in orders:
            amount += order.amount_total

        return {
            'name': account.name,
            'move_id': move.id,
            'account_id': account.id,
            'debit': ((amount > 0) and amount) or 0.0,
            'credit': ((amount < 0) and - amount) or 0.0,
        }
