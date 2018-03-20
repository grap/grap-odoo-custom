# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Multiple Cash Control module for Odoo
#    Copyright (C) 2013 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv.orm import Model


class product_product(Model):
    _inherit = 'product.product'

    # Constraint section
    def _check_pos_ok_res_group(self, cr, uid, ids, context=None):
        ru_obj = self.pool.get('res.users')
        for pp in self.browse(cr, uid, ids, context=context):
            if ((pp.expense_pdt or pp.income_pdt) and
                not ru_obj.has_group(
                    cr, uid, 'account.group_account_manager')):
                return False
        return True

    def _check_purchase_sale_pos_ok(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if ((pp.expense_pdt or pp.income_pdt) and
                    (pp.sale_ok or pp.purchase_ok)):
                return False
        return True

    def _check_pos_purchase_tax(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if (pp.expense_pdt):
                if len(pp.supplier_taxes_id) > 1:
                    return False
        return True

    def _check_pos_property_account_expense(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if (pp.expense_pdt and not pp.property_account_expense):
                return False
        return True

    def _check_pos_property_account_income(self, cr, uid, ids, context=None):
        for pp in self.browse(cr, uid, ids, context=context):
            if (pp.income_pdt and not pp.property_account_income):
                return False
        return True

    _constraints = [
        (
            _check_pos_ok_res_group,
            "You can not create an POS expense or income product if you're"
            " not account manager !",
            ['expense_pdt', 'income_pdt']),
        (
            _check_purchase_sale_pos_ok,
            "You can not create a product that is both salable or purchasable"
            " and POS expense or income product !",
            ['expense_pdt', 'income_pdt', 'sale_ok', 'purchase_ok']),
        (
            _check_pos_purchase_tax,
            "You can not create an POS expense with many taxes !",
            ['expense_pdt', 'supplier_taxes_id']),
        (
            _check_pos_property_account_expense,
            "You can not create an POS expense product without account"
            " expense !",
            ['expense_pdt', 'income_pdt', 'property_account_expense']),
        (
            _check_pos_property_account_income,
            "You can not create an POS income product without account"
            " income !",
            ['expense_pdt', 'income_pdt', 'property_account_expense']),
    ]
