Due to poor design of Odoo Core ``mail`` and ``account`` modules,
the wizard to send mail via odoo is fully duplicated.

* ``mail.xxx``
* ``account.account_invoice_send_wizard_form``

It so forces us to inherit from ``account`` module, and to duplicates
the code.
