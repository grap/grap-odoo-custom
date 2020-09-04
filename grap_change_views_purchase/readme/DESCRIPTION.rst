Change default views for the following modules:

- ``purchase``
- ``purchase_discount``
- ``purchase_triple_discount``


features
--------

- Rename some fields in the puchase order form
- hide unused ``discount3`` field and extra tab in purchase order form
- move ``date_planned`` field from the extra tab near to ``date_order`` field
- make ``taxes_id`` readonly for non accountant people in purchase order view
- merge both menu entries "Requests for Quotation" and "Purchase Orders"
- set red purchase order lines with null amount

- ``date_planned`` field of the order is now, not a computed field anymore.
- ``date_planned`` field of the order line are based on the date_planned field on the order,
  when confirming the order.

Note
----

- hidden fields are available for member of the group ``base.group_erp_manager``
