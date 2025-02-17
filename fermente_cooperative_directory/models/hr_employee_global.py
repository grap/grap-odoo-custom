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

    birthday = fields.Date()

    company_id = fields.Many2one(comodel_name="res.company")

    employee_id = fields.Many2one(comodel_name="hr.employee")

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
                hr_employee.birthday,
                hr_employee.company_id,
                hr_employee.id as employee_id
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
