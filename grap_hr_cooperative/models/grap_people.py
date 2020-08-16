# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class GrapPeople(models.Model):
    _inherit = "grap.people"
    _description = "GRAP Peoples"

    emp_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Employee",
        help="Employee linked to the coop people.")

    @api.model
    def _get_adress_name(self, name, zip, city):
        adress_name = str(name)
        if city != 'False':
            adress_name += " - " + city
        if zip != 'False':
            adress_name += " (" + zip + ")"
        return adress_name

    @api.multi
    def action_get_created_employee(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window'].for_xml_id(
            'hr', 'open_view_employee_list')
        action['res_id'] = self.mapped('emp_id').ids[0]
        return action

    @api.multi
    def create_employee_from_coop_people(self):
        """ Create an hr.employee from the grap.cooperative people """
        employee = False
        for coop_people in self:

            # have to create res.partner to get adress..
            partner_adress_id = self.env['res.partner'].create({
                'is_company': False,
                'name': self._get_adress_name(str(coop_people.name),
                                              str(coop_people.zip),
                                              str(coop_people.city)),
                'email': coop_people.working_email,
                'mobile': coop_people.private_phone,
                'street': coop_people.street,
                'zip': coop_people.zip,
                'city': coop_people.city,
            })
            address_id = partner_adress_id.address_get(['contact'])['contact']

            if coop_people.activity_ids[0:]:
                worker_activity = coop_people.activity_ids[0].activity_id.id
            else:
                worker_activity = False
            employee = self.env['hr.employee'].create({
                'name': coop_people.name,
                'image': coop_people.image,
                'worker_activity': worker_activity,
                'address_home_id': address_id,
                'work_email': coop_people.working_email,
                'work_phone': coop_people.working_phone,
                'birthday': coop_people.birthdate})
            coop_people.write({'emp_id': employee.id})

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        dict_act_window['context'] = {'form_view_initial_mode': 'edit'}
        dict_act_window['res_id'] = employee.id
        return dict_act_window
