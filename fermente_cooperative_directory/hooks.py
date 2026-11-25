import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    _hide_technical_employees(cr)
    _hook_recompute_company_qty(cr)


def _hide_technical_employees(cr):
    _logger.info("hide from directories employee related to 'admin' user")
    cr.execute(
        """
        UPDATE hr_employee
            SET is_displayed_in_directory = false
            WHERE user_id = (
                SELECT res_id
                FROM ir_model_data
                WHERE name = 'user_admin'
                AND module='base'
            );
    """
    )


def _hook_recompute_company_qty(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})

    categories = env["res.company.category"].with_context(active_test=False).search([])
    _logger.info("res_company_category_active: recompute company quantity")
    categories._compute_company_qty()
