# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools


class ResCompany(models.Model):
    _name = "hr.employee.global"
    _description = "Public HR employees Data"
    _auto = False

    name = fields.Char()

    firstname = fields.Char()

    lastname = fields.Char()

    image_1920 = fields.Image(related="employee_id.image_1920")

    image_1024 = fields.Image(related="employee_id.image_1024")

    image_512 = fields.Image(related="employee_id.image_512")

    image_256 = fields.Image(related="employee_id.image_256")

    image_128 = fields.Image(related="employee_id.image_128")

    work_email = fields.Char()

    mobile_phone = fields.Char()

    work_phone = fields.Char()

    company_id = fields.Many2one(comodel_name="res.company")

    employee_id = fields.Many2one(comodel_name="hr.employee")

    birthday = fields.Date(string="Birthday (Private)", groups="hr.group_hr_manager")

    address_home_street = fields.Char(
        string="Street (Private)", groups="hr.group_hr_manager"
    )

    address_home_street2 = fields.Char(
        string="Street 2 (Private)", groups="hr.group_hr_manager"
    )

    address_home_city = fields.Char(
        string="City (Private)", groups="hr.group_hr_manager"
    )

    address_home_state_id = fields.Many2one(
        string="State (Private)",
        comodel_name="res.country.state",
        ondelete="restrict",
        groups="hr.group_hr_manager",
    )

    address_home_zip = fields.Char(string="ZIP (Private)", groups="hr.group_hr_manager")

    address_home_country_id = fields.Many2one(
        string="Country (Private)",
        comodel_name="res.country",
        ondelete="restrict",
        groups="hr.group_hr_manager",
    )

    address_home_phone = fields.Char(
        string="Phone (Private)", groups="hr.group_hr_manager"
    )

    address_home_mobile = fields.Char(
        string="Mobile (Private)", groups="hr.group_hr_manager"
    )

    address_home_email = fields.Char(
        string="Email (Private)", groups="hr.group_hr_manager"
    )

    @api.model
    def _select(self):
        return """
            SELECT
                hr_employee.id as id,
                hr_employee.name,
                hr_employee.firstname,
                hr_employee.lastname,
                hr_employee.work_email,
                hr_employee.mobile_phone,
                hr_employee.work_phone,
                hr_employee.company_id,
                hr_employee.id as employee_id,
                hr_employee.birthday,
                hr_employee.address_home_street,
                hr_employee.address_home_street2,
                hr_employee.address_home_city,
                hr_employee.address_home_state_id,
                hr_employee.address_home_zip,
                hr_employee.address_home_country_id,
                hr_employee.address_home_phone,
                hr_employee.address_home_mobile,
                hr_employee.address_home_email
        """

    @api.model
    def _from(self):
        return """FROM hr_employee"""

    def _join(self):
        return """"""

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)

        self.env.cr.execute(
            f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                {self._select()}
                {self._from()}
                {self._join()}
            )
        """
        )
