Due to poor design of Odoo Core ``mail`` and ``account`` modules,
the wizard to send mail via odoo is fully duplicated.

* ``mail.email_compose_message_wizard_form``
* ``account.account_invoice_send_wizard_form``

see ``fermente_account`` module for the ``account`` changes.
