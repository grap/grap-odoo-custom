* Set a default Document template for all companies. (``web.external_layout_standard``)

Reports Changes
---------------

- Add a field ``price_total_displayed`` on ``account.invoice.line``, that will be the price subtotal
  without taxes, if taxes are price excluded, or the price subtotal with taxes, if taxes are price included.
  This field is displayed on the ``account.invoice`` report.

- When generating invoices from delivered sale orders, add the date of the delivery for each
  ``account.invoice.line``.

- Add ``valuation`` on ``stock.inventory`` report.

- Add a new report for ``product.product`` to have small

Headers / Footers Changes
-------------------------

TODO

PoS Tickets changes
-------------------

Add extra information on PoS Tickets.

[TODO] - add detailled lines for taxes. (Name / Base / amount)
[TODO] - Add customer name and pricelist name. (if not the default one)
