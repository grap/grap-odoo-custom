This module extend Odoo functionnalities, changing and adding decimal precisions.

*  Add a new precision 'GRAP Cost Price' (3 digits), used in:

    * ``account_invoice.margin``
    * ``account_invoice.margin_signed``

    * ``account_invoice_line.margin``
    * ``account_invoice_line.margin_signed``
    * ``account_invoice_line.purchase_price``

    * ``pos_order.margin``

    * ``pos_order.margin``
    * ``pos_order.purchase_price``

    * ``product_product.standard_price``
    * ``product_product.standard_price_tax_included``

    * ``product_template.standard_price``


* Add a new precision 'GRAP Stock Volume' (3 digits), used in:

    * ``product_product.volume``

    * ``product_template.volume``


* Change Precision to 'Stock Weight' (from 2 to 3 digits).
