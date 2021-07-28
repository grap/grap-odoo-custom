# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: DUPONT Quentin (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):

    # Add column
    cr.execute(
        """
        ALTER TABLE res_partner ADD COLUMN partner_type_selec varchar;
    """
    )

    # Populate
    cr.execute(
        """
        UPDATE res_partner
        SET partner_type_selec = 'customer'
        WHERE res_partner.customer = true
        AND res_partner.supplier = false;
    """
    )

    cr.execute(
        """
        UPDATE res_partner
        SET partner_type_selec = 'supplier'
        WHERE res_partner.customer = false
        AND res_partner.supplier = true;
    """
    )

    cr.execute(
        """
        UPDATE res_partner
        SET partner_type_selec = 'customer_supplier'
        WHERE res_partner.customer = true
        AND res_partner.supplier = true;
    """
    )

    cr.execute(
        """
        UPDATE res_partner
        SET partner_type_selec = 'none'
        WHERE res_partner.customer = false
        AND res_partner.supplier = false;
    """
    )
