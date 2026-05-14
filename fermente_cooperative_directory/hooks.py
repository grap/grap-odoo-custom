import logging

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    _hide_technical_employees(cr)


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
