Change default views for the following modules:

- ``account``
- ``account_invoice_triple_discount``
- ``account_invoice_supplierinfo_update_standard_price``

features
--------

- Rename some fields in the account invoice form
- hide unused ``discount3`` field
- move some fields
- make ``invoice_line_tax_ids`` readonly for non accountant people in account invoice views
- set red account invoice lines with null amount

- add colored background in supplier info update wizard

Note
----

- hidden fields are available for member of the group ``base.group_erp_manager``
