This module extends the functionality of mail and email_template module to
changes default email templates that doesn't fit with GRAP needs.

The reason to not change the odoo template is that we have translation
trouble, when changing data, and because default email templates are set
to ``noupdate`` and should be changed, by UI.

Model Changes
~~~~~~~~~~~~~

**email.template**

* add new ``active`` field


Mail Templates
~~~~~~~~~~~~~~

* Disable default Odoo mail templates for ``purchase.order``, ``sale.order``,
  and ``account.invoice``.

* Create new mail templates customized for GRAP. Return these templates, when
  clicking on 'Send by email' button, on each models.

Limited access
~~~~~~~~~~~~~~

This module prevent sending erp link to partners (for quotations, invoices, etc...)
