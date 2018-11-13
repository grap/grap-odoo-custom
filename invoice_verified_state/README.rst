.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3


=============================================
GRAP - Invoices 'Verified' / 'To Check' state
=============================================

1. Add a 'Verified' state on account.invoice (supplier and supplier refund
   invoices)

* Only Accounting managers can validate supplier account invoices
* the workflow is so modified

2. Add a 'To check' checkbox field on account move

* The setting is done per journal
* if a journal is set to 'To Check' all the accounting moves will be set as
  'To Check'. this feature is usefull with the module to export to EBP, to
  prevent import of moves that has not been controled by accounting managers.

Roadmap / Known Issues
======================

* rename the module into ```grap_invoice_state```

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>
* Julien WESTE
