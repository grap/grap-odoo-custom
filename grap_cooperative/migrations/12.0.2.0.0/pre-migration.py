# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):

    cr.execute(
        """
        ALTER TABLE grap_people ADD COLUMN name varchar;
    """
    )

    cr.execute(
        """
        UPDATE grap_people
        SET name = grap_member.name
        FROM grap_member
        WHERE grap_people.grap_member_id = grap_member.id;
    """
    )
