# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: DUPONT Quentin (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):

    # Compute fields for grap.people from grap.member
    cr.execute(
        """
        ALTER TABLE grap_people ADD COLUMN name varchar;
        ALTER TABLE grap_people ADD COLUMN street varchar;
        ALTER TABLE grap_people ADD COLUMN zip varchar;
        ALTER TABLE grap_people ADD COLUMN city varchar;
        ALTER TABLE grap_people ADD COLUMN working_email varchar;
        ALTER TABLE grap_people ADD COLUMN working_phone varchar;
        ALTER TABLE grap_people ADD COLUMN company_id integer;
    """
    )

    cr.execute(
        """
        UPDATE grap_people
        SET name = grap_member.name,
            street = grap_member.street,
            zip = grap_member.zip,
            city = grap_member.city,
            working_email = grap_member.working_email,
            working_phone = grap_member.working_phone
        FROM grap_member
        WHERE grap_people.grap_member_id = grap_member.id;
    """
    )

    # Compute fields for res_company from grap.activity
    cr.execute(
        """
        ALTER TABLE res_company ADD COLUMN accounting_interlocutor_service_id integer;
        ALTER TABLE res_company ADD COLUMN hr_interlocutor_service_id integer;
        ALTER TABLE res_company ADD COLUMN attendant_interlocutor_service_id integer;
    """
    )

    cr.execute(
        """
        UPDATE res_company
        SET accounting_interlocutor_service_id = ga.accountant_interlocutor_id,
            hr_interlocutor_service_id = ga.hr_interlocutor_id,
            attendant_interlocutor_service_id =ga.attendant_interlocutor_id
        FROM grap_activity ga
        WHERE res_company.name ILIKE ('%' || ga.activity_name || '%');
    """
    )

    # Compute res_company from old grap_people.activity_description
    cr.execute(
        """
        UPDATE grap_people
        SET company_id = res_company.id
        FROM res_company
        WHERE res_company.name ILIKE ('%' || grap_people.activity_description || '%');
    """
    )

    # Compute image with ir_attachment
    cr.execute(
        """
        UPDATE ir_attachment
        SET res_model= 'grap.people',
            res_id = grap_people.id
        FROM grap_people
        WHERE ir_attachment.res_id = grap_people.grap_member_id and
              res_model = 'grap.member';
        """
    )
