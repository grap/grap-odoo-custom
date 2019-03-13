# -*- coding: utf-8 -*-
# Copyright (C) 2017-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openupgradelib import openupgrade


logger = logging.getLogger('OpenUpgrade.grap_change_views')


def create_tax_ids_description_field(
        cr, table_line_name, field_description, table_tax_rel_name,
        field_line_id, field_tax_id):
    logger.info(
        "Fast creation of the field"
        " %s.%s (pre)" % (table_line_name, field_description))
    cr.execute("""
        ALTER TABLE %s
        ADD COLUMN "%s" VARCHAR""" % (
        table_line_name,
        field_description))

    cr.execute("""
        SELECT %s, array_agg(%s)
        FROM %s GROUP BY %s;""" % (
        field_line_id, field_tax_id,
        table_tax_rel_name, field_line_id))

    mapping = {}
    res = cr.fetchall()
    for line_id, tax_ids in res:
        if str(tax_ids) in mapping.keys():
            mapping[str(tax_ids)].append(line_id)
        else:
            mapping[str(tax_ids)] = [line_id]

    for str_tax_ids, line_ids in mapping.iteritems():
        # compute description
        tax_ids = eval(str_tax_ids)
        cr.execute("""
            SELECT name, description
            FROM account_tax where id in %s""", (tuple(tax_ids),))
        tax_infos = cr.fetchall()
        tax_description = []
        for name, description in tax_infos:
            tax_description.append(description if description else name)
        tax_ids_description = ', '.join(tax_description).replace("'", " ")
        logger.info(
            "Populating %d lines with %s" % (
                len(line_ids), tax_ids_description))
        line_ids.append(0)
        cr.execute("""
            UPDATE %s
            set %s = '%s'
            WHERE id in %s""" % (
            table_line_name,
            field_description,
            tax_ids_description,
            tuple(line_ids)))


@openupgrade.migrate()
def migrate(cr, version):
    # Account Invoice taxes
    create_tax_ids_description_field(
        cr, 'account_invoice_line', 'tax_ids_description',
        'account_invoice_line_tax', 'invoice_line_id', 'tax_id')

    # Purchase Order taxes
    create_tax_ids_description_field(
        cr, 'purchase_order_line', 'tax_ids_description',
        'purchase_order_taxe', 'ord_id', 'tax_id')

    # Sale Order taxes
    create_tax_ids_description_field(
        cr, 'sale_order_line', 'tax_ids_description',
        'sale_order_tax', 'order_line_id', 'tax_id')
