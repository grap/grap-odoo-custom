This module add extra postgresql indexes to speed up SELECT queries.

**"Purchase" performance**

- ``stock_move``, on ``created_purchase_line_id``

**"Sale" performance**

- ``stock_picking``, on ``sale_id``

**"Stock" performance**

- ``stock_move``, on ``inventory_id``
- ``stock_move_line``, on ``picking_id``
- ``stock_picking``, on ``group_id``

**"Point of Sale" performance**

- ``account_bank_statement_line``, on ``pos_statement_id``
- ``pos_order``, on ``returned_order_id`` and ``company_id``
- ``pos_order_line``, on ``order_id``


**"Product" performance**

- ``product_price_history``, on ``product_id``
