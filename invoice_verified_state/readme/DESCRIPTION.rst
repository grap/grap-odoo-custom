This module extends the functionality of account invoices to
changes default behaviour that doesn't fit with GRAP needs.

1. Add a 'Verified' state on ``account.invoice`` (supplier and supplier refund
   invoices)

* Only Accounting managers can validate supplier account invoices
* the workflow is so modified

2. Add a 'To check' checkbox field on ``account move``

* The setting is done per journal
* if a journal is set to 'To Check' all the accounting moves will be set as
  'To Check'. this feature is usefull with the module to export to EBP, to
  prevent import of moves that has not been controled by accounting managers.

3. On the wizard to invoice stock.picking (``stock.invoice.onshipping``), set
   'Group by partner' checked by default
