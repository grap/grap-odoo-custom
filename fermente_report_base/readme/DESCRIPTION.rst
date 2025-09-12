* Set a default Document template for all companies. (``web.external_layout_standard``)

* change the default footer and header for all the reports. (sale orders, invoices, ....)

Reports Changes
---------------

- Add a field ``price_total_displayed`` on ``account.invoice.line``, that will be the price subtotal
  without taxes, if taxes are price excluded, or the price subtotal with taxes, if taxes are price included.
  This field is displayed on the ``account.invoice`` report.

- When generating invoices from delivered sale orders, add the date of the delivery for each
  ``account.invoice.line``.

- Add ``valuation`` on ``stock.inventory`` report.

- Add a new ``product.print.category`` for ``product.product`` and associated qweb templates.

* Add a new template for ``product.product`` to print sheet of barcodes.


PoS Tickets changes
-------------------

Add extra information on PoS Tickets.

* Add detailled lines for taxes. (Name / Base / amount)
* Add customer name
* Add the pricelist name. (if not the default one)
