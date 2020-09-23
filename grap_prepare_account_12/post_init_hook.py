# coding: utf-8
# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.api import Environment
from openerp import SUPERUSER_ID


def initialize_tax_code(env):
    env.cr.execute("""
        UPDATE account_tax_code
        SET for_deposit_line = false,
            for_tax_line = false,
            for_main_line = false;""")

    env.cr.execute("""
        UPDATE account_tax_code
            SET for_deposit_line = true
            WHERE consignment_product_id is not null;""")

    env.cr.execute("""
        UPDATE account_tax_code
        SET for_tax_line = true
        WHERE id IN (
            SELECT tax_code_id FROM account_tax)
        AND for_deposit_line is false;""")

    env.cr.execute("""
        UPDATE account_tax_code
        SET for_main_line = true
        WHERE id IN (
            SELECT base_code_id FROM account_tax)
        AND for_deposit_line is false;""")

    env.cr.execute("""
        UPDATE account_move_line
            SET name = substring(name, 8)
            WHERE name ilike 'T.V.A. %';""")

    env.cr.execute("""
        UPDATE account_move_line
            SET name='TVA achat 5,5% basé sur prix HT'
            WHERE name = 'TVA-HA-5.5-HT - 5,5% Achat (prix HT)';""")

    env.cr.execute("""
        UPDATE account_tax
            SET name='19,6% Achat (prix HT)'
            WHERE name='[old-2013] 19,6% Achat (prix HT)';""")

    env.cr.execute("""
        UPDATE account_move_line
            SET name='19,6% Achat (prix HT)'
            WHERE name='TVA-HA-19.6-HT - 19,6% Achat (prix HT)';""")

    env.cr.execute("""
        UPDATE account_move_line
            SET name ='Ghee artisanal',
            account_id = 19379
            WHERE tax_code_id = 1850 and account_id = 13340;""")


def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    initialize_tax_code(env)
